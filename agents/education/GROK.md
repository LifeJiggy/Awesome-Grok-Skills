---
name: "Education Agent"
version: "2.0.0"
description: "Comprehensive learning management platform covering course creation, learner progress tracking, adaptive assessments, quiz grading, certification, spaced repetition, learning path optimization, gamification, and educational analytics"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["education", "learning", "courses", "assessments", "quizzes", "certification", "lms", "adaptive-learning", "gamification", "analytics"]
category: "education"
personality: "knowledge-mentor"
use_cases:
  - "course creation and publishing"
  - "learner enrollment and progress tracking"
  - "adaptive quiz assessments and grading"
  - "certificate issuance and verification"
  - "spaced repetition for retention"
  - "personalized learning paths"
  - "gamification and engagement"
  - "educational analytics and reporting"
  - "at-risk learner identification"
---

# Education Agent

> Adaptive learning platform that personalizes education for every learner.

## Table of Contents

- [Agent Identity](#agent-identity)
- [Core Principles](#core-principles)
- [System Architecture](#system-architecture)
- [Capabilities](#capabilities)
- [Data Models](#data-models)
- [Method Signatures](#method-signatures)
- [Operational Guidelines](#operational-guidelines)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Design Patterns](#design-patterns)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Integration Points](#integration-points)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## Agent Identity

The Education Agent is a knowledge mentor that creates personalized learning
experiences. It adapts content difficulty, optimizes learning paths, tracks
progress with precision, and uses science-backed techniques like spaced
repetition and gamification to maximize knowledge retention.

**Core Personality**: Patient, adaptive, evidence-based. Every recommendation
is grounded in learning science. Celebrates progress while pushing growth.

### Agent Capabilities Matrix

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        EDUCATION AGENT CAPABILITIES                        │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Course     │  │  Learner    │  │  Quiz       │  │  Cert       │   │
│  │  Manager    │  │  Manager    │  │  Engine     │  │  Manager    │   │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • Create   │  │  • Profile  │  │  • Create   │  │  • Issue    │   │
│  │  • Publish  │  │  • Enroll   │  │  • Grade    │  │  • Verify   │   │
│  │  • Archive  │  │  • Progress │  │  • Analyze  │  │  • Revoke   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Spaced    │  │  Learning   │  │  Gamifi-    │  │  Analytics  │   │
│  │  Repetition│  │  Path       │  │  cation     │  │  Reporting  │   │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • SM-2     │  │  • Personal │  │  • Points   │  │  • Course   │   │
│  │  • Review   │  │  • Optimize │  │  • Badges   │  │  • Learner  │   │
│  │  • Retention│  │  • Style    │  │  • Ranks    │  │  • Platform │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Core Principles

1. **Learner-Centric**: Every decision optimizes for learner outcomes.
2. **Adaptive Difficulty**: Content matches the learner's current level.
3. **Science-Backed**: Use spaced repetition, retrieval practice, and
   interleaving backed by cognitive science.
4. **Measurable Outcomes**: Track everything — progress, engagement, mastery.
5. **Inclusive Design**: Support all learning styles and accessibility needs.

---

## System Architecture

### High-Level Component Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         EDUCATION AGENT                                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    LEARNING LIFECYCLE                              │   │
│  │  Create → Publish → Enroll → Learn → Assess → Certify            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Course    │ │  Learner   │ │  Quiz      │ │  Cert      │           │
│  │  Manager   │ │  Manager   │ │  Engine    │ │  Manager   │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Spaced   │ │  Learning  │ │  Gamifi-   │ │  Analytics │           │
│  │  Repetition│ │  Path      │ │  cation    │ │  Reporting │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    DATA LAYER (In-Memory + Optional DB)           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Learning Flow Diagram

```
  Learner Journey:
  ════════════════

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Discover │ ─► │ Enroll   │ ─► │ Learn    │ ─► │ Assess   │
  │ Course   │    │          │    │          │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Browse   │    │ Profile  │    │ Complete │    │ Quiz     │
  │ Catalog  │    │ Create   │    │ Lessons  │    │ Grade    │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                              │
                                              ▼
                                       ┌──────────┐    ┌──────────┐
                                       │ Pass?    │ ─► │ Cert     │
                                       │          │    │ Issue    │
                                       └──────────┘    └──────────┘
```

### Course Structure Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                         COURSE                                    │
├─────────────────────────────────────────────────────────────────┤
│  Module 1: Getting Started                                       │
│  ├── Lesson 1.1: Introduction (Video, 15min)                    │
│  ├── Lesson 1.2: Setup Guide (Text, 10min)                      │
│  ├── Lesson 1.3: First Exercise (Interactive, 20min)            │
│  └── Quiz 1: Basics (10 questions)                              │
│                                                                  │
│  Module 2: Core Concepts                                         │
│  ├── Lesson 2.1: Theory (Video, 20min)                          │
│  ├── Lesson 2.2: Practice (Lab, 30min)                          │
│  └── Quiz 2: Concepts (15 questions)                            │
│                                                                  │
│  Module 3: Advanced Topics                                       │
│  ├── Lesson 3.1: Deep Dive (Video, 25min)                       │
│  ├── Lesson 3.2: Project (Assignment, 60min)                    │
│  └── Quiz 3: Mastery (20 questions)                             │
│                                                                  │
│  Final Exam: Comprehensive (50 questions)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Capabilities

### 1. Course Creation & Management

```python
from agents.education.agent import (
    EducationAgent, LessonType, DifficultyLevel, CourseStatus
)

agent = EducationAgent()

# Create a structured course
result = agent.create_course_with_content(
    title="Python Programming Masterclass",
    description="From zero to professional developer",
    instructor_id="inst_001",
    modules_data=[
        {
            "title": "Getting Started",
            "description": "Python basics",
            "lessons": [
                {"title": "What is Python?", "type": "video", "duration": 15},
                {"title": "Installing Python", "type": "text", "duration": 10},
                {"title": "Your First Program", "type": "interactive", "duration": 20},
            ],
        },
        {
            "title": "Data Types",
            "lessons": [
                {"title": "Variables", "type": "video", "duration": 20},
                {"title": "Lists and Tuples", "type": "text", "duration": 15},
            ],
        },
    ],
)
# {"course_id": "course_xxx", "title": "...", "modules": 2, "status": "published"}
```

**Supported Lesson Types**: Video, Text, Interactive, Quiz, Assignment,
Discussion, Lab, Podcast, Document, Live Session.

**Difficulty Levels**: Beginner, Intermediate, Advanced, Expert.

### 2. Learner Enrollment & Progress

```python
# Create learner profile
profile = agent.learner_manager.create_learner_profile(
    name="Alice Johnson",
    email="alice@example.com",
    preferred_style=LearningStyle.VISUAL,
)

# Enroll in course
enrollment = agent.learner_manager.enroll_learner(course.course_id, profile.learner_id)

# Track progress
agent.learner_manager.update_progress(enrollment.enrollment_id, lesson1.lesson_id)
agent.learner_manager.update_progress(enrollment.enrollment_id, lesson2.lesson_id)
agent.learner_manager.record_time_spent(enrollment.enrollment_id, minutes=30)

# Get dashboard
dashboard = agent.learner_manager.get_learner_dashboard(profile.learner_id)
# {"completed": 2, "in_progress": 1, "total_time_hours": 4.5, "points": 150}
```

### 3. Adaptive Quiz Assessments

```python
# Create quiz
quiz = agent.quiz_engine.create_quiz(
    title="Python Basics Quiz",
    course_id=course.course_id,
    passing_score=70,
    time_limit_minutes=30,
    max_attempts=3,
)

# Add questions
agent.quiz_engine.add_question(
    quiz.quiz_id,
    "What keyword defines a function in Python?",
    ["func", "define", "def", "function"],
    correct_index=2,
    points=10,
    explanation="The 'def' keyword defines a function in Python.",
)

# Grade submission
attempt = agent.quiz_engine.grade_quiz(
    quiz.quiz_id, profile.learner_id, {"q_1": 2}
)
print(f"Score: {attempt.percentage}%, Passed: {attempt.passed}")

# Analytics
analytics = agent.quiz_engine.get_quiz_analytics(quiz.quiz_id)
# {"average_score": 82.5, "pass_rate": 75.0, "question_stats": {...}}
```

### 4. Certification

```python
# Issue certificate
cert = agent.cert_manager.issue_certificate(
    learner_id=profile.learner_id,
    course_id=course.course_id,
    learner_name="Alice Johnson",
    course_name="Python Programming Masterclass",
    instructor_name="Dr. Smith",
    final_grade=92.5,
)

# Verify
verification = agent.cert_manager.verify_certificate(cert.certificate_number)
# {"valid": True, "learner_name": "Alice Johnson", "course_name": "..."}

# Get all certificates
certs = agent.cert_manager.get_learner_certificates(profile.learner_id)
```

### 5. Spaced Repetition

```python
# Add item to SRS
item = agent.spaced_repetition.add_item(profile.learner_id, content_id="lesson_001")

# Record review with quality (0-5)
agent.spaced_repetition.record_review(item.item_id, quality=4)  # Easy recall
agent.spaced_repetition.record_review(item.item_id, quality=3)  # Good recall

# Get due items for review
due = agent.spaced_repetition.get_due_items(profile.learner_id)
print(f"Items due for review: {len(due)}")

# Retention stats
stats = agent.spaced_repetition.get_retention_stats(profile.learner_id)
# {"total_items": 25, "due_for_review": 5, "average_memory_strength": 3.2}
```

### 6. Learning Path Optimization

```python
# Create personalized learning path
path = agent.path_optimizer.create_learning_path(
    learner_id=profile.learner_id,
    course_id=course.course_id,
    learner_profile=profile,
)
print(f"Estimated duration: {path.estimated_duration_hours} hours")
print(f"Checkpoints: {len(path.checkpoints)}")

# Optimize for learning style
agent.path_optimizer.optimize_for_style(path.path_id, LearningStyle.KINESTHETIC)
```

### 7. Gamification

```python
# Create achievements
agent.gamification.create_achievement(
    name="First Steps",
    description="Complete your first lesson",
    points=50,
    criteria={"lessons_completed": 1},
    rarity="common",
)

# Award achievement
agent.gamification.award_achievement(profile.learner_id, "ach_001")

# Add points
agent.gamification.add_points(profile.learner_id, 25, GamificationAction.QUIZ_PASSED)

# Leaderboard
board = agent.gamification.get_leaderboard(top_n=10)
# [{"rank": 1, "learner_id": "...", "points": 500}, ...]
```

### 8. Analytics & Reporting

```python
# Course analytics
course_stats = agent.analytics.get_course_analytics(course.course_id)
# {"total_enrollments": 150, "completion_rate": 65.3, "average_progress": 72.1}

# Learner analytics
learner_stats = agent.analytics.get_learner_analytics(profile.learner_id)
# {"completed_courses": 3, "total_time_hours": 45.2, "average_progress": 85.0}

# Platform overview
platform = agent.analytics.get_platform_overview()
# {"total_courses": 50, "total_learners": 5000, "overall_completion_rate": 62.5}

# At-risk identification
at_risk = agent.analytics.identify_at_risk_learners(threshold_days=14)
# [{"learner_id": "...", "days_inactive": 21, "progress": 45.0}]
```

---

## Data Models

### Course Model

```python
@dataclass
class Course:
    course_id: str               # Unique identifier
    title: str                   # Course title
    description: str             # Course description
    instructor_id: str           # Instructor reference
    status: CourseStatus         # DRAFT, PUBLISHED, ARCHIVED
    difficulty: DifficultyLevel  # BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    modules: List[Module]        # Course modules
    price: float                 # Course price
    created_at: datetime
    updated_at: datetime
```

### Module Model

```python
@dataclass
class Module:
    module_id: str               # Unique identifier
    title: str                   # Module title
    description: str             # Module description
    order: int                   # Display order
    lessons: List[Lesson]        # Module lessons
```

### Lesson Model

```python
@dataclass
class Lesson:
    lesson_id: str               # Unique identifier
    title: str                   # Lesson title
    content: str                 # Lesson content/URL
    lesson_type: LessonType      # VIDEO, TEXT, INTERACTIVE, etc.
    duration_minutes: int        # Estimated duration
    difficulty: DifficultyLevel  # Difficulty level
    order: int                   # Display order
```

### LearnerProfile Model

```python
@dataclass
class LearnerProfile:
    learner_id: str              # Unique identifier
    name: str                    # Learner name
    email: str                   # Email address
    preferred_style: LearningStyle  # VISUAL, AUDITORY, etc.
    skills: List[str]            # Known skills
    points: int                  # Gamification points
    created_at: datetime
```

### Enrollment Model

```python
@dataclass
class Enrollment:
    enrollment_id: str           # Unique identifier
    learner_id: str              # Learner reference
    course_id: str               # Course reference
    status: EnrollmentStatus     # ACTIVE, COMPLETED, DROPPED
    progress: float              # 0-100 percentage
    time_spent_minutes: int      # Total time spent
    enrolled_at: datetime
    completed_at: Optional[datetime]
```

### Quiz Model

```python
@dataclass
class Quiz:
    quiz_id: str                 # Unique identifier
    title: str                   # Quiz title
    course_id: str               # Parent course
    questions: List[Question]    # Quiz questions
    passing_score: float         # Minimum score to pass (0-100)
    time_limit_minutes: int      # Time limit
    max_attempts: int            # Maximum attempts
```

### Question Model

```python
@dataclass
class Question:
    question_id: str             # Unique identifier
    question_text: str           # Question text
    options: List[str]           # Answer options
    correct_index: int           # Correct answer index
    points: int                  # Points value
    explanation: str             # Correct answer explanation
```

### Certificate Model

```python
@dataclass
class Certificate:
    certificate_id: str          # Unique identifier
    certificate_number: str      # Human-readable number
    learner_id: str              # Learner reference
    course_id: str               # Course reference
    learner_name: str            # Learner name
    course_name: str             # Course name
    instructor_name: str         # Instructor name
    final_grade: float           # Final grade (0-100)
    issued_at: datetime          # Issue date
    expires_at: Optional[datetime]  # Expiry date
    status: CertStatus           # VALID, REVOKED, EXPIRED
```

### SpacedRepetitionItem Model

```python
@dataclass
class SpacedRepetitionItem:
    item_id: str                 # Unique identifier
    learner_id: str              # Learner reference
    content_id: str              # Content reference
    ease_factor: float           # SM-2 ease factor (default 2.5)
    interval_days: int           # Days until next review
    repetition_count: int        # Number of reviews
    next_review: datetime        # Next review date
    last_quality: int            # Last quality rating (0-5)
```

### Data Model Relationships

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Course    │ 1───∞ │    Module    │ 1───∞ │    Lesson    │
│              │       │              │       │              │
│ course_id    │       │ module_id    │       │ lesson_id    │
│ title        │       │ title        │       │ title        │
│ instructor_id│       │ order        │       │ type         │
│ status       │       └──────────────┘       │ duration     │
└──────┬───────┘                              └──────────────┘
       │
       │ 1───∞
       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Enrollment  │ ∞───1 │   Learner    │ 1───∞ │ Certificate  │
│              │       │   Profile    │       │              │
│ enrollment_id│       │ learner_id   │       │ cert_id      │
│ learner_id  ─┼──────►│ name         │       │ learner_id   │
│ course_id    │       │ email        │       │ course_id    │
│ progress     │       │ style        │       │ grade        │
│ status       │       │ points       │       │ status       │
└──────────────┘       └──────────────┘       └──────────────┘
       │
       │ 1───∞
       ▼
┌──────────────┐
│    Quiz      │ 1───∞ ┌──────────────┐
│              │       │  Question    │
│ quiz_id      │       │              │
│ course_id    │       │ question_id  │
│ passing_score│       │ text         │
│ time_limit   │       │ options      │
└──────────────┘       │ correct_index│
                       └──────────────┘
```

---

## Method Signatures

### EducationAgent (Top-Level)

```python
def create_course_with_content(
    self,
    title: str,
    description: str,
    instructor_id: str,
    modules_data: List[Dict[str, Any]],
) -> Dict[str, Any]

def get_education_dashboard(self) -> Dict[str, Any]

def get_status(self) -> Dict[str, Any]
```

### CourseManager

```python
def create_course(
    self,
    title: str,
    description: str,
    instructor_id: str,
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
    price: float = 0.0,
) -> Course

def update_course(self, course_id: str, updates: Dict[str, Any]) -> Optional[Course]

def get_course(self, course_id: str) -> Optional[Course]

def delete_course(self, course_id: str) -> bool

def add_module(
    self,
    course_id: str,
    title: str,
    description: str = "",
    order: int = 0,
) -> Optional[Module]

def add_lesson(
    self,
    module_id: str,
    title: str,
    content: str,
    lesson_type: LessonType = LessonType.TEXT,
    duration_minutes: int = 10,
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
    order: int = 0,
) -> Optional[Lesson]

def publish_course(self, course_id: str) -> bool

def archive_course(self, course_id: str) -> bool

def get_course_details(self, course_id: str) -> Optional[Dict[str, Any]]

def get_course_catalog(
    self,
    category: Optional[str] = None,
    difficulty: Optional[DifficultyLevel] = None,
    published_only: bool = True,
) -> List[Dict[str, Any]]
```

### LearnerManager

```python
def create_learner_profile(
    self,
    name: str,
    email: str,
    preferred_style: LearningStyle = LearningStyle.VISUAL,
) -> LearnerProfile

def enroll_learner(
    self,
    course_id: str,
    learner_id: str,
) -> Optional[Enrollment]

def update_progress(
    self,
    enrollment_id: str,
    lesson_id: str,
    completed: bool = True,
) -> Optional[Enrollment]

def record_time_spent(self, enrollment_id: str, minutes: int) -> None

def get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]

def get_learner_enrollments(self, learner_id: str) -> List[Enrollment]

def get_learner_dashboard(self, learner_id: str) -> Dict[str, Any]
```

### QuizEngine

```python
def create_quiz(
    self,
    title: str,
    course_id: str,
    passing_score: float = 70,
    time_limit_minutes: int = 30,
    max_attempts: int = 3,
) -> Quiz

def add_question(
    self,
    quiz_id: str,
    question_text: str,
    options: List[str],
    correct_index: int,
    points: int = 10,
    explanation: str = "",
) -> Optional[str]

def grade_quiz(
    self,
    quiz_id: str,
    learner_id: str,
    answers: Dict[str, int],
) -> Optional[QuizAttempt]

def get_quiz_results(self, quiz_id: str, learner_id: str) -> List[QuizAttempt]

def get_quiz_analytics(self, quiz_id: str) -> Dict[str, Any]
```

### CertificationManager

```python
def issue_certificate(
    self,
    learner_id: str,
    course_id: str,
    learner_name: str,
    course_name: str,
    instructor_name: str,
    final_grade: float = 100.0,
) -> Certificate

def verify_certificate(self, certificate_number: str) -> Dict[str, Any]

def revoke_certificate(self, certificate_id: str, reason: str = "") -> bool

def get_learner_certificates(self, learner_id: str) -> List[Certificate]
```

### SpacedRepetitionEngine

```python
def add_item(self, learner_id: str, content_id: str) -> SpacedRepetitionItem

def record_review(self, item_id: str, quality: int) -> Optional[SpacedRepetitionItem]

def get_due_items(self, learner_id: str) -> List[SpacedRepetitionItem]

def get_retention_stats(self, learner_id: str) -> Dict[str, Any]
```

### LearningPathOptimizer

```python
def create_learning_path(
    self,
    learner_id: str,
    course_id: str,
    learner_profile: Optional[LearnerProfile] = None,
) -> Optional[LearningPath]

def get_path(self, path_id: str) -> Optional[LearningPath]

def optimize_for_style(
    self,
    path_id: str,
    learning_style: LearningStyle,
) -> Optional[LearningPath]
```

### GamificationEngine

```python
def create_achievement(
    self,
    name: str,
    description: str,
    points: int,
    criteria: Dict[str, Any],
    rarity: str = "common",
) -> Achievement

def award_achievement(self, learner_id: str, achievement_id: str) -> bool

def add_points(self, learner_id: str, points: int, action: GamificationAction) -> None

def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]

def get_learner_achievements(self, learner_id: str) -> List[Dict[str, Any]]

def get_learner_points(self, learner_id: str) -> int
```

### AnalyticsReporting

```python
def get_course_analytics(self, course_id: str) -> Dict[str, Any]

def get_learner_analytics(self, learner_id: str) -> Dict[str, Any]

def get_platform_overview(self) -> Dict[str, Any]

def identify_at_risk_learners(self, threshold_days: int = 7) -> List[Dict[str, Any]]
```

---

## Operational Guidelines

### Course Design Checklist

1. Define clear learning objectives (Bloom's taxonomy levels)
2. Structure content into logical modules
3. Mix lesson types (video + text + interactive)
4. Keep lessons under 20 minutes for engagement
5. Include assessments after each module
6. Set appropriate passing scores (70%+ recommended)
7. Add supplementary resources (PDFs, links, code samples)
8. Test the full learner journey before publishing

### Assessment Best Practices

- Use multiple question types per quiz
- Include explanations for correct answers
- Set reasonable time limits (not too tight)
- Limit attempts to 3 to prevent guessing
- Randomize question order to reduce cheating
- Review question analytics to improve weak items

### Spaced Repetition Tuning

- Quality 4-5: Material is well-known → extend interval
- Quality 3: Remembered with effort → maintain interval
- Quality 0-2: Forgotten → reset to 1 day
- Review due items daily for best retention
- Target 80%+ retention probability

### Gamification Strategy

- Award points for consistent activity (streaks)
- Create achievements for milestones (1st lesson, 10 quizzes, etc.)
- Use rarity tiers to create aspiration
- Update leaderboards frequently to maintain motivation
- Balance extrinsic rewards with intrinsic motivation

---

## Configuration

### Agent Configuration

```yaml
education_agent:
  course_manager:
    max_courses: 50000
    auto_save_drafts: true
    default_difficulty: beginner

  learner_manager:
    inactivity_threshold_days: 7
    streak_grace_period_hours: 24
    max_enrollments_per_learner: 50

  quiz_engine:
    default_time_limit_minutes: 30
    max_attempts_default: 3
    randomize_questions: true
    passing_score_default: 70

  certification:
    certificate_validity_months: 24
    use_digital_signature: true
    certificate_template: "default"

  spaced_repetition:
    max_items_per_learner: 1000
    default_ease_factor: 2.5
    review_window_days: 30

  gamification:
    points_per_lesson: 10
    points_per_quiz_pass: 25
    streak_bonus_multiplier: 1.5
    achievement_rarities:
      common: 50
      uncommon: 100
      rare: 200
      epic: 500
      legendary: 1000

  analytics:
    at_risk_threshold_days: 14
    engagement_score_weights:
      completion: 0.4
      time_spent: 0.3
      quiz_scores: 0.2
      activity: 0.1
```

---

## Security Considerations

### Data Protection

- Encrypt learner PII (name, email) at rest
- Implement proper authentication for admin endpoints
- Use rate limiting on quiz submission endpoints
- Validate all input to prevent injection attacks
- Log all certification issuances for audit

### Assessment Integrity

- Randomize question order per attempt
- Implement time limits to prevent lookup
- Limit attempts to prevent brute-force guessing
- Use question banks for large quiz pools
- Track suspicious patterns (rapid perfect scores)

### Certification Security

- Generate unique certificate numbers
- Implement digital signatures for certificates
- Support certificate verification API
- Maintain revocation list for compromised certificates
- Log all certificate operations

---

## Scalability

### Current Design Limits

| Component | Limit | Notes |
|-----------|-------|-------|
| Courses | ~10,000 | In-memory storage |
| Learners | ~100,000 | Per session |
| Quiz questions | ~1,000 | Per quiz |
| Concurrent users | ~100 | Single process |

### Scaling Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                    SCALING PATHWAY                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Phase 1: In-Memory (Current)                                │
│  ├── Single process, stdlib only                             │
│  └── Suitable for < 1000 learners                            │
│                                                               │
│  Phase 2: Database Backend                                   │
│  ├── PostgreSQL/MySQL for persistence                        │
│  ├── Redis for session caching                               │
│  └── Suitable for < 50K learners                             │
│                                                               │
│  Phase 3: Distributed                                        │
│  ├── Microservices per component                             │
│  ├── CDN for video content                                   │
│  ├── Message queues for async grading                        │
│  └── Suitable for 50K+ learners                              │
│                                                               │
│  Phase 4: Global Scale                                       │
│  ├── Multi-region deployment                                 │
│  ├── Edge caching for content                                │
│  ├── Database sharding by learner                            │
│  └── Suitable for 1M+ learners                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Performance Benchmarks

| Operation | Current | With DB | With Cache |
|-----------|---------|---------|------------|
| Course search (1K courses) | ~5ms | ~20ms | ~2ms |
| Quiz grading (50 questions) | ~10ms | ~30ms | ~15ms |
| Progress update | ~1ms | ~5ms | ~2ms |
| Analytics query | ~20ms | ~50ms | ~10ms |
| Certificate verification | ~2ms | ~10ms | ~2ms |

---

## Design Patterns

### Strategy Pattern

Different learning path optimization strategies are interchangeable:

```python
class LearningStrategy(ABC):
    @abstractmethod
    def optimize(self, learner: LearnerProfile, course: Course) -> List[str]:
        pass

class VisualFirstStrategy(LearningStrategy):
    def optimize(self, learner, course):
        # Prioritize video and interactive content
        return sorted(course.lessons, key=lambda l: 
            0 if l.type in ("video", "interactive") else 1)

class TextFirstStrategy(LearningStrategy):
    def optimize(self, learner, course):
        # Prioritize text content
        return sorted(course.lessons, key=lambda l:
            0 if l.type == "text" else 1)
```

### Observer Pattern

Progress changes trigger notifications:

```python
class ProgressObserver(ABC):
    @abstractmethod
    def on_progress_updated(self, enrollment: Enrollment, lesson: Lesson):
        pass

class AchievementChecker(ProgressObserver):
    def on_progress_updated(self, enrollment, lesson):
        if enrollment.progress == 100:
            self.award_completion_achievement(enrollment)

class NotificationSender(ProgressObserver):
    def on_progress_updated(self, enrollment, lesson):
        self.send_lesson_complete_email(enrollment, lesson)
```

### Template Method Pattern

Quiz grading follows a common template with type-specific variations:

```python
class QuizGrader(ABC):
    def grade(self, quiz: Quiz, answers: Dict) -> QuizAttempt:
        score = self.calculate_score(quiz, answers)
        passed = score >= quiz.passing_score
        return QuizAttempt(score=score, passed=passed, ...)

    @abstractmethod
    def calculate_score(self, quiz: Quiz, answers: Dict) -> float:
        pass

class MultipleChoiceGrader(QuizGrader):
    def calculate_score(self, quiz, answers):
        correct = sum(1 for q in quiz.questions 
                     if answers.get(q.id) == q.correct_index)
        return (correct / len(quiz.questions)) * 100
```

### State Pattern

Enrollment status transitions:

```python
class EnrollmentState(ABC):
    @abstractmethod
    def next(self, enrollment: Enrollment) -> 'EnrollmentState':
        pass

class ActiveState(EnrollmentState):
    def next(self, enrollment):
        if enrollment.progress == 100:
            return CompletedState()
        return self

class CompletedState(EnrollmentState):
    def next(self, enrollment):
        return self  # Terminal state
```

---

## Checklists

### Course Creation Checklist

- [ ] Learning objectives defined (Bloom's taxonomy)
- [ ] Modules structured logically (easy → hard)
- [ ] Mix of lesson types for engagement
- [ ] Assessments included after each module
- [ ] Passing scores set appropriately (70%+)
- [ ] Certificate template configured
- [ ] Supplementary resources added
- [ ] Full learner journey tested

### Quiz Design Checklist

- [ ] Questions aligned with learning objectives
- [ ] Mix of question types (MC, true/false, etc.)
- [ ] Clear, unambiguous question wording
- [ ] Correct answers verified
- [ ] Explanations provided for all questions
- [ ] Time limits set appropriately
- [ ] Max attempts configured
- [ ] Question order randomized

### Learner Support Checklist

- [ ] Onboarding flow documented
- [ ] Help resources accessible
- [ ] Contact support configured
- [ ] Progress tracking visible
- [ ] Achievements and rewards clear
- [ ] At-risk monitoring enabled
- [ ] Intervention emails configured

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Course won't publish | Validation errors | Run `validate()` and fix issues |
| Progress not updating | Enrollment not found | Verify enrollment_id is correct |
| Quiz won't grade | Max attempts reached | Check `max_attempts` setting |
| Certificate invalid | Expired or revoked | Check `certificate_number` and status |
| SRS items not appearing | No items added | Call `add_item()` before `get_due_items()` |
| At-risk list empty | All learners active | Lower `threshold_days` parameter |
| Gamification points 0 | No achievements awarded | Award achievements via `award_achievement()` |
| Enrollment stuck | Missing lesson completion | Ensure all lessons are marked complete |
| Quiz score incorrect | Wrong answer mapping | Verify correct_index values |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed course info
details = agent.course_manager.get_course_details(course_id)
print(f"Modules: {len(details['modules'])}")
print(f"Lessons: {sum(len(m['lessons']) for m in details['modules'])}")
```

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| Moodle | LTI | LMS integration |
| Canvas | LTI | LMS integration |
| Vimeo | REST API | Video hosting |
| Stripe | REST API | Payment for courses |
| SendGrid | REST API | Learner notifications |
| Google Analytics | GA4 | Learning analytics |
| Proctorio | API | Exam proctoring |
| Zoom | API | Live sessions |
| Slack | API | Community integration |

---

## Examples

### Example 1: Complete Learner Journey

```python
agent = EducationAgent()

# Create course
result = agent.create_course_with_content(
    title="Web Development Bootcamp",
    description="Full-stack web development",
    instructor_id="inst_001",
    modules_data=[...],
)

# Learner enrolls
profile = agent.learner_manager.create_learner_profile("Charlie", "charlie@example.com")
enrollment = agent.learner_manager.enroll_learner(result["course_id"], profile.learner_id)

# Learner completes lessons
for lesson_id in lesson_ids:
    agent.learner_manager.update_progress(enrollment.enrollment_id, lesson_id)

# Learner passes quiz
quiz = agent.quiz_engine.create_quiz("Module 1 Quiz", result["course_id"])
agent.quiz_engine.add_question(quiz.quiz_id, "What does HTML stand for?", [...], 0)
attempt = agent.quiz_engine.grade_quiz(quiz.quiz_id, profile.learner_id, {"q_1": 0})

# Certificate issued
cert = agent.cert_manager.issue_certificate(
    profile.learner_id, result["course_id"], "Charlie", "Web Dev Bootcamp", "Dr. Smith"
)
```

### Example 2: Spaced Repetition Study Session

```python
# Add key concepts to SRS
for concept in ["variables", "functions", "loops", "classes"]:
    agent.spaced_repetition.add_item(profile.learner_id, concept)

# Study session
due_items = agent.spaced_repetition.get_due_items(profile.learner_id)
for item in due_items:
    quality = get_learner_response_quality()  # 0-5
    agent.spaced_repetition.record_review(item.item_id, quality)

# Check retention
stats = agent.spaced_repetition.get_retention_stats(profile.learner_id)
print(f"Items due: {stats['due_for_review']}")
print(f"Avg memory strength: {stats['average_memory_strength']:.1f}")
```

### Example 3: At-Risk Intervention

```python
# Weekly at-risk check
at_risk = agent.analytics.identify_at_risk_learners(threshold_days=14)
for learner in at_risk:
    print(f"Intervene: {learner['learner_id']} "
          f"(inactive {learner['days_inactive']} days, "
          f"progress {learner['progress']}%)")
    # Send intervention email
    send_intervention_email(learner["learner_id"], learner["course_id"])
```

---

## Best Practices

1. **Structure courses logically** — easy concepts first, build complexity.
2. **Keep lessons short** — 10-20 minutes max for engagement.
3. **Mix content types** — video + text + interactive for different styles.
4. **Assess frequently** — quiz after each module, not just at the end.
5. **Use spaced repetition** — key concepts reviewed at optimal intervals.
6. **Gamify thoughtfully** — points and achievements drive motivation.
7. **Monitor at-risk learners** — intervene before they drop off.
8. **Gather feedback** — improve courses based on analytics.
9. **Set realistic time estimates** — help learners plan their study time.
10. **Celebrate completions** — certificates and recognition matter.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[README.md](./README.md) for quick start and API reference.
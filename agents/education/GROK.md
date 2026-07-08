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

## Agent Identity

The Education Agent is a knowledge mentor that creates personalized learning
experiences. It adapts content difficulty, optimizes learning paths, tracks
progress with precision, and uses science-backed techniques like spaced
repetition and gamification to maximize knowledge retention.

**Core Personality**: Patient, adaptive, evidence-based. Every recommendation
is grounded in learning science. Celebrates progress while pushing growth.

## Core Principles

1. **Learner-Centric**: Every decision optimizes for learner outcomes.
2. **Adaptive Difficulty**: Content matches the learner's current level.
3. **Science-Backed**: Use spaced repetition, retrieval practice, and
   interleaving backed by cognitive science.
4. **Measurable Outcomes**: Track everything — progress, engagement, mastery.
5. **Inclusive Design**: Support all learning styles and accessibility needs.

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

## Method Signatures

### CourseManager

```python
def create_course(self, title, description, instructor_id, ...) -> Course
def update_course(self, course_id, updates) -> Optional[Course]
def get_course(self, course_id) -> Optional[Course]
def delete_course(self, course_id) -> bool
def add_module(self, course_id, title, description="", order=0) -> Optional[Module]
def add_lesson(self, module_id, title, content, lesson_type=LessonType.TEXT, ...) -> Optional[Lesson]
def publish_course(self, course_id) -> bool
def archive_course(self, course_id) -> bool
def get_course_details(self, course_id) -> Optional[Dict]
def get_course_catalog(self, category=None, difficulty=None, published_only=True) -> List[Dict]
```

### LearnerManager

```python
def create_learner_profile(self, name, email, preferred_style=...) -> LearnerProfile
def enroll_learner(self, course_id, learner_id) -> Optional[Enrollment]
def update_progress(self, enrollment_id, lesson_id, completed=True) -> Optional[Enrollment]
def record_time_spent(self, enrollment_id, minutes) -> None
def get_enrollment(self, enrollment_id) -> Optional[Enrollment]
def get_learner_enrollments(self, learner_id) -> List[Enrollment]
def get_learner_dashboard(self, learner_id) -> Dict
```

### QuizEngine

```python
def create_quiz(self, title, course_id, passing_score=70, ...) -> Quiz
def add_question(self, quiz_id, question_text, options, correct_index, ...) -> Optional[str]
def grade_quiz(self, quiz_id, learner_id, answers) -> Optional[QuizAttempt]
def get_quiz_results(self, quiz_id, learner_id) -> List[QuizAttempt]
def get_quiz_analytics(self, quiz_id) -> Dict
```

### CertificationManager

```python
def issue_certificate(self, learner_id, course_id, learner_name, ...) -> Certificate
def verify_certificate(self, certificate_number) -> Dict
def revoke_certificate(self, certificate_id, reason="") -> bool
def get_learner_certificates(self, learner_id) -> List[Certificate]
```

### SpacedRepetitionEngine

```python
def add_item(self, learner_id, content_id) -> SpacedRepetitionItem
def record_review(self, item_id, quality) -> Optional[SpacedRepetitionItem]
def get_due_items(self, learner_id) -> List[SpacedRepetitionItem]
def get_retention_stats(self, learner_id) -> Dict
```

### LearningPathOptimizer

```python
def create_learning_path(self, learner_id, course_id, learner_profile=None) -> Optional[LearningPath]
def get_path(self, path_id) -> Optional[LearningPath]
def optimize_for_style(self, path_id, learning_style) -> Optional[LearningPath]
```

### GamificationEngine

```python
def create_achievement(self, name, description, points, criteria, rarity="common") -> Achievement
def award_achievement(self, learner_id, achievement_id) -> bool
def add_points(self, learner_id, points, action) -> None
def get_leaderboard(self, top_n=10) -> List[Dict]
def get_learner_achievements(self, learner_id) -> List[Dict]
def get_learner_points(self, learner_id) -> int
```

### AnalyticsReporting

```python
def get_course_analytics(self, course_id) -> Dict
def get_learner_analytics(self, learner_id) -> Dict
def get_platform_overview(self) -> Dict
def identify_at_risk_learners(self, threshold_days=7) -> List[Dict]
```

---

## Usage Patterns

### Pattern 1: Full Course Launch

```python
agent = EducationAgent()
result = agent.create_course_with_content(
    title="Data Science 101",
    description="Introduction to data science",
    instructor_id="inst_002",
    modules_data=[...],
)
# Course auto-published
```

### Pattern 2: Learner Journey

```python
profile = agent.learner_manager.create_learner_profile("Bob", "bob@example.com")
enrollment = agent.learner_manager.enroll_learner(course_id, profile.learner_id)
# ... learner completes lessons ...
agent.learner_manager.update_progress(enrollment.id, lesson_id)
# ... learner completes all lessons ...
cert = agent.cert_manager.issue_certificate(profile.learner_id, course_id, "Bob", "Data Science 101", "Dr. Jones")
```

### Pattern 3: At-Risk Intervention

```python
at_risk = agent.analytics.identify_at_risk_learners(threshold_days=14)
for learner in at_risk:
    send_intervention_email(learner["learner_id"], learner["course_id"])
```

---

## Data Models Reference

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| Course | Course container | id, title, instructor, modules, status, price |
| Module | Content grouping | id, title, order, lessons |
| Lesson | Individual content | id, type, content, duration, difficulty |
| Quiz | Assessment | id, questions, passing_score, time_limit |
| QuizAttempt | Grading result | id, answers, score, percentage, passed |
| Enrollment | Learner-course link | id, status, progress, time_spent |
| Certificate | Completion proof | id, number, issued_at, status |
| LearnerProfile | Learner data | id, name, style, skills, points |
| LearningPath | Personalized path | id, modules_order, checkpoints |
| SpacedRepetitionItem | SRS card | id, interval, ease_factor, next_review |
| Achievement | Gamification badge | id, name, points, rarity |
| EngagementMetrics | Activity data | sessions, time, completions |

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Course won't publish | Validation errors | Run `validate()` and fix issues |
| Progress not updating | Enrollment not found | Verify enrollment_id is correct |
| Quiz won't grade | Max attempts reached | Check `max_attempts` setting |
| Certificate invalid | Expired or revoked | Check `certificate_number` and status |
| SRS items not appearing | No items added | Call `add_item()` before `get_due_items()` |
| At-risk list empty | All learners active | Lower `threshold_days` parameter |
| Gamification points 0 | No achievements awarded | Award achievements via `award_achievement()` |

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

---

## Checklist

- [ ] Course objectives defined with Bloom's taxonomy levels
- [ ] Modules structured logically (easy → hard)
- [ ] Mix of lesson types for engagement
- [ ] Assessments included after each module
- [ ] Passing scores set appropriately
- [ ] Certificate template configured
- [ ] Spaced repetition items added for key concepts
- [ ] Gamification achievements created
- [ ] Analytics dashboards configured
- [ ] At-risk learner monitoring enabled

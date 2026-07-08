# Education Agent

Comprehensive learning management platform covering course creation, learner
progress tracking, adaptive assessments, quiz grading, certification, spaced
repetition, learning path optimization, gamification, and educational analytics.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Education Agent provides a complete learning management system built with
modular sub-engines. It supports the full educational lifecycle — from course
design through learner completion and certification — with adaptive learning
features grounded in cognitive science.

Each sub-engine (Course, Learner, Quiz, Certification, Spaced Repetition,
Learning Path, Gamification, Analytics) operates independently while being
orchestrated by a top-level agent for unified operations.

---

## Features

### Course Management
- Create courses with modules and lessons
- 10 lesson types (video, text, interactive, quiz, assignment, lab, etc.)
- 4 difficulty levels (beginner to expert)
- Course publishing and archiving workflow
- Course catalog with filtering

### Learner Management
- Learner profile creation with learning style preference
- Course enrollment and progress tracking
- Time spent tracking
- Learner dashboard with activity summary
- At-risk learner identification

### Adaptive Assessments
- 10 assessment types (multiple choice, essay, coding, etc.)
- Configurable passing scores and time limits
- Multi-attempt support with attempt tracking
- Per-question feedback and explanations
- Quiz analytics with question-level statistics

### Certification
- Certificate issuance with unique numbering
- Certificate verification
- Revocation support
- Expiration handling

### Spaced Repetition
- SM-2 algorithm for optimal review scheduling
- Memory strength and ease factor tracking
- Due item identification
- Retention probability calculation

### Learning Path Optimization
- Personalized learning path generation
- Checkpoint-based progress tracking
- Learning style adaptation
- Estimated duration calculation

### Gamification
- Achievement system with rarity tiers
- Points and leaderboard tracking
- Streak management
- Multiple achievement criteria

### Analytics
- Course-level analytics (enrollments, completion, ratings)
- Learner-level analytics (progress, time, skills)
- Platform overview dashboard
- At-risk learner identification

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  EducationAgent                       │
├──────────────────────────────────────────────────────┤
│  CourseManager │ LearnerManager │ QuizEngine         │
│  CertificationManager │ SpacedRepetitionEngine       │
│  LearningPathOptimizer │ GamificationEngine          │
│  AnalyticsReporting                                 │
└──────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed component diagrams,
data flows, and design patterns.

---

## Quick Start

```python
from agents.education.agent import EducationAgent, LessonType, DifficultyLevel

agent = EducationAgent()

# Create and publish a course
result = agent.create_course_with_content(
    title="Intro to AI",
    description="Learn artificial intelligence fundamentals",
    instructor_id="inst_001",
    modules_data=[
        {
            "title": "What is AI?",
            "lessons": [
                {"title": "History of AI", "type": "video", "duration": 20},
                {"title": "AI Today", "type": "text", "duration": 15},
            ],
        },
    ],
)
print(f"Course published: {result['course_id']}")
```

---

## Installation

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -r requirements.txt
python agents/education/agent.py
```

---

## Usage

### Running the Demo

```bash
python agents/education/agent.py
```

Demonstrates course creation, learner enrollment, progress tracking, quiz
grading, certification, and analytics.

### Programmatic Usage

```python
from agents.education.agent import EducationAgent

agent = EducationAgent()

# Check agent status
print(agent.get_status())

# Get platform dashboard
dashboard = agent.get_education_dashboard()
print(f"Courses: {dashboard['platform']['total_courses']}")
print(f"Learners: {dashboard['platform']['total_learners']}")
```

---

## API Reference

### EducationAgent (Top-Level)

| Method | Description | Returns |
|--------|-------------|---------|
| `create_course_with_content(...)` | Create + publish course | `Dict` |
| `get_education_dashboard()` | Platform dashboard | `Dict` |
| `get_status()` | Agent status | `Dict` |

### CourseManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_course(title, desc, instructor_id, ...)` | Create course | `Course` |
| `update_course(id, updates)` | Update course | `Course` |
| `get_course(id)` | Get course | `Course` |
| `delete_course(id)` | Delete course | `bool` |
| `add_module(course_id, title, ...)` | Add module | `Module` |
| `add_lesson(module_id, title, content, ...)` | Add lesson | `Lesson` |
| `publish_course(id)` | Publish | `bool` |
| `archive_course(id)` | Archive | `bool` |
| `get_course_details(id)` | Full details | `Dict` |
| `get_course_catalog(...)` | Browse catalog | `List[Dict]` |

### LearnerManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_learner_profile(name, email, style)` | Create profile | `LearnerProfile` |
| `enroll_learner(course_id, learner_id)` | Enroll | `Enrollment` |
| `update_progress(enrollment_id, lesson_id, completed)` | Update progress | `Enrollment` |
| `record_time_spent(enrollment_id, minutes)` | Record time | `None` |
| `get_learner_dashboard(learner_id)` | Dashboard | `Dict` |

### QuizEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `create_quiz(title, course_id, ...)` | Create quiz | `Quiz` |
| `add_question(quiz_id, text, options, correct, ...)` | Add question | `str` |
| `grade_quiz(quiz_id, learner_id, answers)` | Grade | `QuizAttempt` |
| `get_quiz_results(quiz_id, learner_id)` | Get results | `List[QuizAttempt]` |
| `get_quiz_analytics(quiz_id)` | Analytics | `Dict` |

### CertificationManager

| Method | Description | Returns |
|--------|-------------|---------|
| `issue_certificate(learner_id, course_id, ...)` | Issue cert | `Certificate` |
| `verify_certificate(number)` | Verify | `Dict` |
| `revoke_certificate(id, reason)` | Revoke | `bool` |
| `get_learner_certificates(learner_id)` | List certs | `List[Certificate]` |

### SpacedRepetitionEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `add_item(learner_id, content_id)` | Add item | `SRItem` |
| `record_review(item_id, quality)` | Record review | `SRItem` |
| `get_due_items(learner_id)` | Get due items | `List[SRItem]` |
| `get_retention_stats(learner_id)` | Stats | `Dict` |

### LearningPathOptimizer

| Method | Description | Returns |
|--------|-------------|---------|
| `create_learning_path(learner_id, course_id, ...)` | Create path | `LearningPath` |
| `get_path(path_id)` | Get path | `LearningPath` |
| `optimize_for_style(path_id, style)` | Optimize | `LearningPath` |

### GamificationEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `create_achievement(name, desc, points, criteria, ...)` | Create | `Achievement` |
| `award_achievement(learner_id, achievement_id)` | Award | `bool` |
| `add_points(learner_id, points, action)` | Add points | `None` |
| `get_leaderboard(top_n)` | Leaderboard | `List[Dict]` |
| `get_learner_points(learner_id)` | Points | `int` |

### AnalyticsReporting

| Method | Description | Returns |
|--------|-------------|---------|
| `get_course_analytics(course_id)` | Course stats | `Dict` |
| `get_learner_analytics(learner_id)` | Learner stats | `Dict` |
| `get_platform_overview()` | Platform stats | `Dict` |
| `identify_at_risk_learners(threshold_days)` | At-risk | `List[Dict]` |

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
```

### Example 3: At-Risk Intervention

```python
# Weekly at-risk check
at_risk = agent.analytics.identify_at_risk_learners(threshold_days=14)
for learner in at_risk:
    print(f"Intervene: {learner['learner_id']} "
          f"(inactive {learner['days_inactive']} days, "
          f"progress {learner['progress']}%)")
```

---

## Configuration

```yaml
education_agent:
  course_manager:
    max_courses: 50000
    auto_save_drafts: true

  learner_manager:
    inactivity_threshold_days: 7
    streak_grace_period_hours: 24

  quiz_engine:
    default_time_limit_minutes: 30
    max_attempts_default: 3
    randomize_questions: true

  certification:
    certificate_validity_months: 24
    use_digital_signature: true

  spaced_repetition:
    max_items_per_learner: 1000
    default_ease_factor: 2.5

  gamification:
    points_per_lesson: 10
    points_per_quiz_pass: 25
    streak_bonus_multiplier: 1.5
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

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Course won't publish | Missing required fields | Run `validate()` and fix errors |
| Progress stuck at 0% | Enrollment not started | Complete first lesson to trigger start |
| Quiz score 0% | All answers wrong | Check question data and correct_index |
| Certificate not valid | Expired or revoked | Check status and expiry date |
| SRS items not due | All reviewed recently | Wait for next_review date |
| At-risk list empty | Learners are active | Lower threshold_days |
| Leaderboard empty | No points awarded | Award achievements first |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[GROK.md](./GROK.md) for agent identity and operational guidelines.

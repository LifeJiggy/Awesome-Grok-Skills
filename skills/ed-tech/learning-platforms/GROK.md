---
name: "Learning Platforms"
version: "2.0.0"
description: "Comprehensive learning platform toolkit with course management, content delivery, progress tracking, assessment integration, and learner analytics for educational technology"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ed-tech", "learning-platforms", "course-management", "content-delivery", "learner-analytics"]
category: "ed-tech"
personality: "learning-engineer"
use_cases: ["course management", "content delivery", "progress tracking", "assessment", "learner analytics"]
---

# Learning Platforms

> Production-grade learning platform framework providing course management, content delivery, progress tracking, assessment integration, and learner analytics for building effective educational technology solutions.

## Overview

The Learning Platforms module provides a complete toolkit for building and managing learning management systems. It implements course creation and management, multi-format content delivery, learner progress tracking with xAPI/Caliper, assessment creation and grading, adaptive learning path recommendations, and comprehensive learning analytics. Every feature includes accessibility compliance and mobile-responsive design.

## Core Capabilities

### 1. Course Management
- Course creation and organization
- Module and lesson structuring
- Prerequisite and dependency management
- Enrollment and cohort management
- Certificate generation

### 2. Content Delivery
- Multi-format content support (video, SCORM, HTML5)
- Adaptive streaming for video content
- Offline content access
- Content versioning and updates
- Accessibility compliance (WCAG 2.1)

### 3. Progress Tracking
- xAPI statement generation
- Completion criteria configuration
- Badge and achievement systems
- Learning path progress visualization
- Time tracking and engagement metrics

### 4. Assessment Integration
- Multiple question types (MCQ, essay, code, file upload)
- Auto-grading and manual grading
- Rubric-based assessment
- Proctoring integration
- Question bank management

### 5. Adaptive Learning
- Knowledge gap identification
- Personalized content recommendations
- Difficulty adjustment based on performance
- Spaced repetition scheduling
- Learning style adaptation

### 6. Learning Analytics
- Learner performance dashboards
- Course effectiveness metrics
- Engagement analytics
- Completion rate tracking
- Predictive analytics for at-risk learners

## Usage Examples

### Course Management

```python
from learning_platforms import CourseManager, Course

manager = CourseManager()

# Create a course
course = manager.create_course(
    title="Python Programming Fundamentals",
    description="Learn Python from scratch",
    instructor="jane.smith@company.com",
    duration_hours=40,
    modules=[
        {"title": "Introduction", "lessons": 5},
        {"title": "Data Types", "lessons": 8},
        {"title": "Control Flow", "lessons": 6},
        {"title": "Functions", "lessons": 7},
    ],
)

print(f"Course: {course.title}")
print(f"Modules: {len(course.modules)}")
print(f"Total lessons: {course.total_lessons}")
```

### Progress Tracking

```python
from learning_platforms import ProgressTracker, xAPIStatement

tracker = ProgressTracker()

# Track learning activity
statement = xAPIStatement(
    actor="learner@example.com",
    verb="completed",
    object="lesson-variables",
    result={"score": 85, "time_spent": 300},
)

tracker.record(statement)

# Get learner progress
progress = tracker.get_progress("learner@example.com", course_id="python-101")
print(f"Completion: {progress.completion_pct:.1f}%")
print(f"Time spent: {progress.time_spent_hours:.1f} hours")
print(f"Average score: {progress.avg_score:.1f}%")
```

### Assessment

```python
from learning_platforms import AssessmentEngine, QuestionBank

engine = AssessmentEngine()

# Create assessment
assessment = engine.create_assessment(
    title="Python Basics Quiz",
    questions=20,
    time_limit_minutes=30,
    passing_score=70,
)

# Grade submission
result = engine.grade(
    assessment_id=assessment.id,
    submission={"q1": "A", "q2": "B", "q3": "C"},
)
print(f"Score: {result.score}%")
print(f"Passed: {result.passed}")
print(f"Feedback: {result.feedback}")
```

### Learning Analytics

```python
from learning_platforms import AnalyticsEngine

analytics = AnalyticsEngine()

# Get course analytics
report = analytics.course_report("python-101")
print(f"Enrolled: {report.enrolled_count}")
print(f"Completed: {report.completed_count}")
print(f"Completion rate: {report.completion_rate:.1%}")
print(f"Avg score: {report.avg_score:.1f}%")

# Identify at-risk learners
at_risk = analytics.get_at_risk_learners("python-101")
print(f"At-risk learners: {len(at_risk)}")
for learner in at_risk[:5]:
    print(f"  {learner.email}: {learner.risk_reason}")
```

## Best Practices

### Course Design
- Chunk content into 10-15 minute segments
- Include interactive elements every 5 minutes
- Provide multiple content formats for accessibility
- Set clear learning objectives for each module

### Progress Tracking
- Use xAPI for interoperability
- Track both completion and engagement
- Provide real-time progress feedback
- Celebrate milestones and achievements

### Assessment
- Mix question types for comprehensive evaluation
- Provide immediate feedback where possible
- Use rubrics for consistent grading
- Offer practice assessments before graded ones

### Analytics
- Focus on actionable insights
- Identify at-risk learners early
- Measure course effectiveness, not just completion
- Use data to improve content continuously

## Related Modules

- **adaptive-learning**: Personalized learning paths
- **assessment-systems**: Advanced assessment tools
- **content-delivery**: Content management and delivery
- **student-analytics**: Detailed learner analytics
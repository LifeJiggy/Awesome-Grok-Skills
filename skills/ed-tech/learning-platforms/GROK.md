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

---

## Advanced Configuration

### Environment Variables

```bash
# Core Configuration
LP_DATABASE_URL=postgresql://user:pass@localhost:5432/learning_platform
LP_REDIS_URL=redis://localhost:6379/0
LP_SECRET_KEY=your-secret-key-here
LP_DEBUG=false
LP_LOG_LEVEL=INFO

# Content Delivery
LP_CDN_ENABLED=true
LP_CDN_PROVIDER=cloudfront
LP_STORAGE_BACKEND=s3
LP_STORAGE_BUCKET=edu-content-assets
LP_MAX_UPLOAD_SIZE_MB=500

# Assessment
LP_ASSESSMENT_TIMEOUT_MINUTES=60
LP_PROCTORING_ENABLED=true
LP_AUTO_GRADE_ENABLED=true
LP_QUESTION_BANK_SIZE=10000

# Analytics
LP_ANALYTICS_RETENTION_DAYS=365
LP_PREDICTIVE_MODEL_ENABLED=true
LP_REAL_TIME_ANALYTICS=true
LP_BATCH_PROCESSING_SCHEDULE=0 2 * * *
```

### Feature Flags

```python
from learning_platforms import FeatureFlags

flags = FeatureFlags()

# Toggle features
flags.enable("adaptive_learning")
flags.enable("proctoring")
flags.disable("beta_ai_grading")

# Percentage rollout
flags rollout(
    feature="new_ui",
    percentage=25,
    target_groups=["beta_users", "internal"],
)

# A/B testing
experiment = flags.experiment(
    name="course_layout_test",
    variants=["traditional", "card_based"],
    traffic_split=[50, 50],
)
```

### Advanced Course Configuration

```python
from learning_platforms import CourseConfig

config = CourseConfig(
    # Enrollment
    max_enrollment=500,
    waitlist_enabled=True,
    auto_approve_enrollment=False,
    
    # Completion
    completion_criteria={
        "min_score": 70,
        "required_modules": ["intro", "core", "final"],
        "time_commitment_hours": 20,
    },
    
    # Accessibility
    wcag_level="AA",
    caption_language=["en", "es"],
    screen_reader_optimized=True,
    
    # Certificate
    certificate_template="professional",
    certificate_expiry_months=12,
    verification_url="https://verify.example.com",
)
```

## Architecture Patterns

### Event-Driven Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Learner   │────▶│  API Gateway │────▶│  Auth Service│
│   Portal    │     │              │     │              │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                    ┌──────▼───────┐
                    │  Event Bus   │
                    │  (Kafka)     │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
   ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
   │  Course   │    │ Assessment│    │ Analytics │
   │  Service  │    │  Service  │    │  Service  │
   └───────────┘    └───────────┘    └───────────┘
```

### Microservices Decomposition

- **Course Service**: Manages course CRUD, enrollment, prerequisites
- **Content Service**: Handles multi-format content, streaming, CDN
- **Assessment Service**: Question banks, grading, proctoring
- **Analytics Service**: Event processing, dashboards, predictions
- **Notification Service**: Email, push, in-app notifications
- **Certificate Service**: Generation, verification, revocation

### Caching Strategy

```python
from learning_platforms import CacheManager

cache = CacheManager()

# Multi-tier caching
cache.configure(
    l1_cache="memory",      # In-process LRU cache
    l2_cache="redis",        # Distributed cache
    l3_cache="cdn",          # Edge cache for static content
    ttl_config={
        "course_metadata": 300,      # 5 minutes
        "learner_progress": 60,      # 1 minute
        "static_content": 86400,     # 24 hours
        "assessment_results": 1800,  # 30 minutes
    },
)
```

## Integration Guide

### LTI Integration

```python
from learning_platforms import LTIIntegration

lti = LTIIntegration()

# Register LTI tool
tool = lti.register_tool(
    name="External Assessment Tool",
    consumer_key="lti-consumer-key",
    shared_secret="lti-shared-secret",
    launch_url="https://external-tool.example.com/launch",
    redirect_uris=["https://external-tool.example.com/callback"],
)

# Handle LTI launch
@lti.launch_endpoint
def handle_launch(lti_request):
    user = lti.authenticate(lti_request)
    return redirect(f"/tool/{user.id}/dashboard")
```

### SCORM/xAPI Integration

```python
from learning_platforms import SCORMPackage, xAPIClient

# Package SCORM content
scorm = SCORMPackage(
    source="course_content/",
    manifest="imsmanifest.xml",
    scorm_version="2004",
)

# Package for delivery
package = scorm.package(output_path="output/scorm_package.zip")
print(f"Package size: {package.size_mb:.1f} MB")

# Send xAPI statements
xapi = xAPIClient(endpoint="https://lrs.example.com")

statement = xapi.create_statement(
    actor="learner@example.com",
    verb="completed",
    object_type="activity",
    object_id="https://example.com/activity/123",
    result={
        "score": {"scaled": 0.85},
        "success": True,
        "duration": "PT30M",
    },
)

xapi.send_statement(statement)
```

### SSO Integration

```python
from learning_platforms import SSOProvider

# Configure SAML SSO
saml = SSOProvider(
    provider_type="saml",
    entity_id="https://platform.example.com",
    sso_url="https://idp.example.com/sso",
    certificate="-----BEGIN CERTIFICATE-----\n...",
    sign_requests=True,
)

# Configure OAuth SSO
oauth = SSOProvider(
    provider_type="oauth",
    client_id="your-client-id",
    client_secret="your-client-secret",
    authorization_url="https://auth.example.com/authorize",
    token_url="https://auth.example.com/token",
    scopes=["openid", "profile", "email"],
)
```

## Performance Optimization

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_learner_course ON enrollments(learner_id, course_id);
CREATE INDEX idx_progress_updated ON progress(updated_at);
CREATE INDEX idx_assessment_submitted ON submissions(submitted_at);

-- Partition large tables
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    learner_id UUID NOT NULL,
    activity_id UUID NOT NULL,
    score DECIMAL,
    created_at TIMESTAMP DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE progress_2024_q1 PARTITION OF progress
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

### Query Optimization

```python
from learning_platforms import QueryOptimizer

optimizer = QueryOptimizer()

# Analyze slow queries
slow_queries = optimizer.analyze_slow_queries(
    threshold_ms=100,
    time_range_hours=24,
)

for query in slow_queries:
    print(f"Query: {query.sql[:100]}...")
    print(f"Duration: {query.avg_duration_ms:.0f}ms")
    print(f"Suggestion: {query.optimization_suggestion}")

# Optimize N+1 queries
optimized_query = optimizer.eager_load(
    Course.objects.all(),
    related_fields=["modules", "modules__lessons", "instructor"],
)
```

### Caching Implementation

```python
from learning_platforms import CacheDecorator, invalidate_cache

@CacheDecorator(ttl=300, key_prefix="course")
def get_course_with_stats(course_id):
    course = Course.objects.get(id=course_id)
    stats = CourseStats.objects.get(course_id=course_id)
    return {"course": course, "stats": stats}

@invalidate_cache(pattern="course:*")
def update_course(course_id, data):
    course = Course.objects.get(id=course_id)
    course.update(**data)
    return course
```

## Security Considerations

### Data Encryption

```python
from learning_platforms import EncryptionManager

encryption = EncryptionManager()

# Encrypt sensitive data
encrypted_pii = encryption.encrypt_pii({
    "name": "John Doe",
    "email": "john@example.com",
    "ssn": "123-45-6789",
})

# Hash passwords
password_hash = encryption.hash_password(
    password="user-password",
    algorithm="argon2",
    iterations=3,
)
```

### Access Control

```python
from learning_platforms import RBACManager

rbac = RBACManager()

# Define roles
rbac.define_role("instructor", permissions=[
    "course.create",
    "course.edit",
    "course.delete",
    "assessment.create",
    "assessment.grade",
    "analytics.view_course",
])

rbac.define_role("learner", permissions=[
    "course.view",
    "content.view",
    "assessment.submit",
    "progress.view_own",
])

# Check permissions
can_edit = rbac.check_permission(user, "course.edit", course_id="course-123")
```

### Audit Logging

```python
from learning_platforms import AuditLogger

audit = AuditLogger()

# Log sensitive actions
audit.log(
    action="grade.modified",
    user="instructor@example.com",
    resource_type="assessment_submission",
    resource_id="sub-123",
    details={
        "old_score": 75,
        "new_score": 80,
        "reason": "Re-evaluation of essay question 3",
    },
    ip_address="192.168.1.100",
)

# Query audit logs
logs = audit.query(
    resource_type="assessment_submission",
    date_range=("2024-01-01", "2024-01-31"),
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Content not loading | CDN cache stale | Purge CDN cache, verify origin |
| Slow enrollment | Database lock | Check for long-running transactions |
| SCORM tracking errors | xAPI endpoint down | Verify LRS connectivity |
| Video buffering | Insufficient ABR profiles | Add lower bitrate options |
| Grade sync issues | Race condition | Implement idempotent sync |

### Debug Mode

```python
from learning_platforms import enable_debug

# Enable debug logging
enable_debug(
    components=["auth", "course", "assessment"],
    log_level="DEBUG",
    trace_requests=True,
)

# Debug specific learner
debug_session = debug.track_learner("learner@example.com")
print(f"Session ID: {debug_session.id}")
print(f"Debug URL: {debug_session.debug_url}")
```

### Health Checks

```python
from learning_platforms import HealthCheck

health = HealthCheck()

# Check all services
status = health.check_all()
print(f"Overall: {status.healthy}")
for service in status.services:
    print(f"  {service.name}: {service.status} ({service.latency_ms:.0f}ms)")

# Custom health check
@health.check("custom_assessment_service")
def check_assessment_service():
    # Test database connectivity
    db_ok = test_database_connection()
    # Test external API
    api_ok = test_assessment_api()
    return db_ok and api_ok
```

## API Reference

### REST Endpoints

```
GET    /api/v2/courses                    List courses
POST   /api/v2/courses                    Create course
GET    /api/v2/courses/{id}               Get course details
PUT    /api/v2/courses/{id}               Update course
DELETE /api/v2/courses/{id}               Delete course

GET    /api/v2/courses/{id}/modules       List modules
POST   /api/v2/courses/{id}/modules       Create module
GET    /api/v2/courses/{id}/enrollments   List enrollments
POST   /api/v2/courses/{id}/enrollments   Enroll learner

GET    /api/v2/learners/{id}/progress     Get learner progress
POST   /api/v2/learners/{id}/progress     Record progress
GET    /api/v2/learners/{id}/analytics    Get learner analytics
```

### GraphQL Schema

```graphql
type Course {
  id: ID!
  title: String!
  description: String
  instructor: User!
  modules: [Module!]!
  enrollments: [Enrollment!]!
  stats: CourseStats
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Learner {
  id: ID!
  email: String!
  enrollments: [Enrollment!]!
  progress: [Progress!]!
  certificates: [Certificate!]!
}

type Query {
  course(id: ID!): Course
  courses(filter: CourseFilter, limit: Int, offset: Int): [Course!]!
  learner(id: ID!): Learner
}

type Mutation {
  createCourse(input: CreateCourseInput!): Course!
  enrollLearner(courseId: ID!, learnerId: ID!): Enrollment!
  recordProgress(learnerId: ID!, activityId: ID!, score: Float): Progress!
}
```

## Data Models

### Core Entities

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Course:
    id: UUID
    title: str
    description: Optional[str]
    instructor_id: UUID
    status: str  # draft, published, archived
    created_at: datetime
    updated_at: datetime

@dataclass
class Module:
    id: UUID
    course_id: UUID
    title: str
    order: int
    lessons: List["Lesson"]
    prerequisites: List[UUID]

@dataclass
class Lesson:
    id: UUID
    module_id: UUID
    title: str
    content_type: str  # video, document, interactive
    content_url: str
    duration_minutes: int
    order: int

@dataclass
class Enrollment:
    id: UUID
    learner_id: UUID
    course_id: UUID
    status: str  # active, completed, dropped
    enrolled_at: datetime
    completed_at: Optional[datetime]

@dataclass
class Progress:
    id: UUID
    learner_id: UUID
    activity_id: UUID
    activity_type: str
    score: Optional[float]
    time_spent_seconds: int
    completed: bool
    created_at: datetime
```

### Database Schema

```sql
-- Courses table
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor_id UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Modules table
CREATE TABLE modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enrollments table
CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    status VARCHAR(20) DEFAULT 'active',
    enrolled_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    UNIQUE(learner_id, course_id)
);
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "learning_platforms.app:app", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learning-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: learning-platform
  template:
    metadata:
      labels:
        app: learning-platform
    spec:
      containers:
      - name: api
        image: learning-platform:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: platform-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Learning Platform

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/ --cov=learning_platforms
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build and push Docker image
        run: |
          docker build -t learning-platform:${{ github.sha }} .
          docker push registry.example.com/learning-platform:${{ github.sha }}
          
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/learning-platform \
            api=registry.example.com/learning-platform:${{ github.sha }}
          kubectl rollout status deployment/learning-platform
```

## Monitoring & Observability

### Metrics Collection

```python
from learning_platforms import MetricsCollector, MetricType

metrics = MetricsCollector()

# Custom metrics
metrics.counter("course.enrollments", tags={"course_id": course_id})
metrics.histogram("assessment.duration_seconds", duration, tags={"type": "quiz"})
metrics.gauge("active_learners", count, tags={"course_id": course_id})

# Business metrics
metrics.track_conversion(
    event="learner_progress",
    from_stage="enrolled",
    to_stage="completed",
    value=1.0,
)
```

### Distributed Tracing

```python
from learning_platforms import Tracer

tracer = Tracer(service_name="learning-platform")

# Trace across services
with tracer.span("enrollment_process") as span:
    span.set_tag("learner_id", learner_id)
    span.set_tag("course_id", course_id)
    
    # Database call
    with tracer.span("database_check"):
        existing = check_enrollment(learner_id, course_id)
    
    # External API call
    with tracer.span("payment_api"):
        payment = process_payment(learner_id, course_id)
    
    # Create enrollment
    enrollment = create_enrollment(learner_id, course_id)
```

### Alerting Rules

```yaml
# prometheus/alerts.yml
groups:
- name: learning-platform
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      
  - alert: SlowGrades
    expr: histogram_quantile(0.95, grade_duration_seconds) > 10
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Grade calculation latency high"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from learning_platforms import CourseManager

@pytest.fixture
def course_manager():
    return CourseManager(test_mode=True)

def test_create_course(course_manager):
    course = course_manager.create_course(
        title="Test Course",
        description="A test course",
        instructor="instructor@example.com",
    )
    assert course.id is not None
    assert course.title == "Test Course"
    assert course.status == "draft"

def test_enroll_learner(course_manager):
    course = course_manager.create_course(title="Test Course")
    enrollment = course_manager.enroll_learner(
        course_id=course.id,
        learner_id="learner@example.com",
    )
    assert enrollment.status == "active"
```

### Integration Tests

```python
@pytest.mark.integration
def test_full_enrollment_flow(client, db):
    # Create course
    response = client.post("/api/v2/courses", json={
        "title": "Integration Test Course",
        "description": "Test",
    })
    assert response.status_code == 201
    course_id = response.json()["id"]
    
    # Enroll learner
    response = client.post(f"/api/v2/courses/{course_id}/enrollments", json={
        "learner_id": "learner@example.com",
    })
    assert response.status_code == 201
    
    # Verify enrollment
    response = client.get(f"/api/v2/courses/{course_id}/enrollments")
    assert len(response.json()["results"]) == 1
```

### Load Testing

```python
from locust import HttpUser, task, between

class LearnerUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def view_courses(self):
        self.client.get("/api/v2/courses")
    
    @task(2)
    def view_course(self):
        self.client.get(f"/api/v2/courses/{self.course_id}")
    
    @task(1)
    def submit_assessment(self):
        self.client.post(f"/api/v2/assessments/{self.assessment_id}/submit", json={
            "answers": {"q1": "A", "q2": "B"},
        })
```

## Versioning & Migration

### API Versioning

```python
from learning_platforms import APIVersion

api = APIVersion()

# v2 endpoints (current)
@api.route("/api/v2/courses")
class CourseListV2:
    def get(self):
        return courses_with_stats()

# v1 endpoints (deprecated)
@api.route("/api/v1/courses", deprecated=True)
class CourseListV1:
    def get(self):
        return basic_courses()
```

### Database Migrations

```python
# migrations/001_add_certificates.py
def up(schema):
    schema.create_table("certificates", {
        "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "enrollment_id": "UUID REFERENCES enrollments(id)",
        "issued_at": "TIMESTAMP DEFAULT NOW()",
        "expires_at": "TIMESTAMP",
        "verification_code": "VARCHAR(50) UNIQUE",
    })

def down(schema):
    schema.drop_table("certificates")
```

### Breaking Changes Policy

- Deprecate with 6-month notice
- Support minimum 2 major versions
- Provide migration guides
- Maintain backwards compatibility layer

## Glossary

| Term | Definition |
|------|------------|
| **xAPI** | Experience API - standard for tracking learning experiences |
| **SCORM** | Sharable Content Object Reference Model - e-learning standard |
| **LTI** | Learning Tools Interoperability - standard for integrating tools |
| **ABR** | Adaptive Bitrate - streaming quality adjustment based on bandwidth |
| **LRS** | Learning Record Store - stores xAPI statements |
| **WCAG** | Web Content Accessibility Guidelines |
| **LMS** | Learning Management System |
| **Cohort** | Group of learners progressing together |
| **Rubric** | Scoring guide for subjective assessments |
| **Formative** | Ongoing assessment during learning |
| **Summative** | Final assessment of learning |

## Changelog

### Version 2.0.0 (Current)
- Added adaptive learning recommendations
- Implemented xAPI 1.0.3 support
- Added proctoring integration
- Improved analytics dashboards
- Added SCORM 2004 4th Edition support

### Version 1.5.0
- Added certificate generation
- Implemented bulk enrollment
- Added course templates
- Improved mobile responsiveness

### Version 1.0.0
- Initial release
- Course management
- Basic assessments
- Progress tracking
- Content delivery

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Update documentation
6. Submit pull request

### Code Standards
- Follow PEP 8 style guide
- Write docstrings for public APIs
- Maintain 80%+ test coverage
- Use type hints throughout

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---
name: "tutorials"
category: "technical-writing"
version: "1.0.0"
tags: ["technical-writing", "tutorials", "learning-paths", "assessment", "interactive"]
---

# Progressive Tutorial Authoring & Learning Path Design

## Overview

Effective tutorials transform novices into practitioners through carefully sequenced, hands-on learning experiences. This module provides a structured framework for authoring progressive tutorials, designing learning paths with prerequisite tracking, building interactive coding exercises, generating assessments, and measuring tutorial effectiveness through analytics.

The core principle is progressive disclosure: each tutorial builds on previously established knowledge without assuming expertise the reader hasn't acquired yet. The module enforces this through prerequisite graphs, skill trees, and content complexity scoring. When a tutorial references a concept, the system verifies that the prerequisite tutorial covering that concept appears earlier in the learning path.

Interactive tutorials are supported through embedded code runners, validation functions, and hint systems. Each exercise includes a problem statement, starter code, solution validator, and progressive hints that reveal gradually as the learner struggles. The assessment engine generates quizzes from tutorial content using template-based question generation, spaced repetition scheduling, and adaptive difficulty adjustment.

Multi-language support enables the same conceptual tutorial to be authored once and rendered with code examples in Python, JavaScript, TypeScript, Go, or Rust. The tutorial system maintains a shared concept layer independent of implementation language, with language-specific code blocks that can be toggled by the reader.

The analytics subsystem tracks learner behavior across tutorials: completion rates per step, exercise pass rates, hint usage patterns, and time-to-completion distributions. These metrics feed back into tutorial improvement cycles, helping authors identify where content is confusing, where exercises are too difficult, and where learners lose motivation.

## Core Capabilities

- **Progressive Tutorial Authoring**: Structure tutorials with clear learning objectives, step-by-step instructions, code exercises, and knowledge checks using a consistent template system.
- **Learning Path Design**: Create multi-tutorial learning paths with prerequisite graphs, estimated completion times, difficulty progression, and skill tree visualization.
- **Interactive Coding Exercises**: Embed executable code validators, hint systems, and sandboxed code runners within tutorials for hands-on practice.
- **Assessment Generation**: Auto-generate quizzes, coding challenges, and knowledge checks from tutorial content with configurable difficulty levels and question types.
- **Prerequisite Tracking**: Model prerequisite relationships as directed acyclic graphs and validate that learning paths maintain correct ordering.
- **Multi-Language Support**: Author tutorial concepts once and render code examples in multiple programming languages with consistent structure.
- **Effectiveness Analytics**: Track tutorial completion rates, exercise success rates, hint usage, and time-to-completion to identify improvement opportunities.
- **Skill Tree Construction**: Map tutorial content to skill trees with proficiency levels, enabling learners to visualize their progress and identify gaps.

## Usage Examples

### Tutorial Authoring

```python
from tutorials import Tutorial, TutorialStep, Exercise

tutorial = Tutorial(
    id="intro-python-functions",
    title="Introduction to Python Functions",
    difficulty="beginner",
    estimated_minutes=30,
    learning_objectives=[
        "Define functions with parameters and return values",
        "Understand scope and variable lifetime",
        "Write functions that process lists"
    ]
)

tutorial.add_step(TutorialStep(
    order=1,
    title="Your First Function",
    content="""
    A function is a reusable block of code. Define one using the `def` keyword:
    ```python
    def greet(name):
        return f"Hello, {name}!"
    ```
    """,
    exercise=Exercise(
        type="coding",
        prompt="Write a function called `square` that takes a number and returns its square.",
        starter_code="def square(n):\n    # Your code here\n    pass",
        validator=lambda code: "return" in code and "n *" in code or "n **" in code or "n**2" in code,
        hints=["Think about the * operator", "Try: return n * n"]
    )
))

tutorial.add_step(TutorialStep(
    order=2,
    title="Functions with Default Parameters",
    content="You can set default values for parameters...",
    prerequisites=["intro-python-basics"]
))

print(tutorial.to_markdown())
```

### Learning Path Design

```python
from tutorials import LearningPath, SkillNode

path = LearningPath(
    id="python-backend",
    title="Python Backend Development",
    description="Go from zero to building production APIs"
)

path.add_module("fundamentals", [
    SkillNode(id="python-basics", title="Python Basics", minutes=120),
    SkillNode(id="python-functions", title="Functions & Modules", minutes=90,
              prerequisites=["python-basics"]),
    SkillNode(id="python-oop", title="Object-Oriented Python", minutes=150,
              prerequisites=["python-functions"]),
])

path.add_module("web", [
    SkillNode(id="http-fundamentals", title="HTTP Fundamentals", minutes=60),
    SkillNode(id="flask-intro", title="Introduction to Flask", minutes=120,
              prerequisites=["python-functions", "http-fundamentals"]),
    SkillNode(id="flask-advanced", title="Advanced Flask Patterns", minutes=180,
              prerequisites=["flask-intro", "python-oop"]),
])

# Validate path ordering
issues = path.validate()
for issue in issues:
    print(f"  {issue.severity}: {issue.message}")

# Generate visual skill tree
path.render_skill_tree(output="skill-tree.html")
```

### Interactive Exercise with Validation

```python
from tutorials import InteractiveExercise, HintLevel

exercise = InteractiveExercise(
    id="list-comprehension",
    title="List Comprehensions",
    language="python",
    problem="""
    Given a list of numbers, use a list comprehension to create a new list
    containing only the even numbers, each squared.
    
    Input: [1, 2, 3, 4, 5, 6]
    Expected: [4, 16, 36]
    """,
    starter_code="def even_squares(numbers):\n    # Use a list comprehension\n    pass",
    test_cases=[
        {"input": [1, 2, 3, 4, 5, 6], "expected": [4, 16, 36]},
        {"input": [0, 1, 2], "expected": [0, 4]},
        {"input": [], "expected": []},
    ],
    hints=[
        HintLevel(text="Remember: [expr for item in iterable if condition]", level=1),
        HintLevel(text="Use: [n**2 for n in numbers if n % 2 == 0]", level=2),
        HintLevel(text="Full solution: def even_squares(numbers): return [n**2 for n in numbers if n % 2 == 0]", level=3),
    ],
    concepts=["list-comprehensions", "filtering", "exponentiation"]
)

# Validate student submission
result = exercise.validate("def even_squares(numbers):\n    return [n**2 for n in numbers if n % 2 == 0]")
print(f"Passed: {result.passed}")
print(f"Tests: {result.tests_passed}/{result.tests_total}")
```

### Assessment Generation

```python
from tutorials import AssessmentEngine, QuestionType

engine = AssessmentEngine(
    tutorials=["intro-python-functions", "intro-python-oop"],
    question_types=[QuestionType.MULTIPLE_CHOICE, QuestionType.CODE_COMPLETION],
    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2}
)

# Generate a 10-question assessment
assessment = engine.generate(num_questions=10)
print(f"Generated {len(assessment.questions)} questions")
for q in assessment.questions:
    print(f"  [{q.difficulty}] {q.type.value}: {q.stem[:80]}...")

# Score a submission
score = engine.score(assessment, submission={
    "q1": "A function defined with def",
    "q2": "return x + y",
    "q3": "B",
})
print(f"Score: {score.correct}/{score.total} ({score.percentage:.1f}%)")
```

### Effectiveness Analytics

```python
from tutorials import TutorialAnalytics

analytics = TutorialAnalytics(data_dir="analytics/")

# Analyze a specific tutorial
report = analytics.analyze("intro-python-functions")
print(f"Completion rate: {report.completion_rate:.1%}")
print(f"Avg time: {report.avg_completion_minutes:.0f} min")
print(f"Exercise pass rate: {report.exercise_pass_rate:.1%}")
print(f"Hint usage: {report.hint_usage_rate:.1%}")

# Identify struggling points
for pain_point in report.pain_points:
    print(f"  PAIN: Step {pain_point.step_order} — {pain_point.failure_rate:.0%} failure rate")
    print(f"    Common errors: {', '.join(pain_point.common_errors[:3])}")
```

## Best Practices

1. **Start with a working example**: Begin every tutorial with a complete, runnable example that demonstrates the end goal. Then deconstruct it step by step.
2. **Enforce prerequisite ordering**: Always validate that learners have completed prerequisite content before introducing advanced concepts. Broken prerequisite chains confuse learners.
3. **One concept per step**: Each tutorial step should teach exactly one new concept. If a step requires multiple new ideas, split it into separate steps.
4. **Make exercises runnable**: Every code exercise should have a validator that checks the learner's solution automatically. Silent failures in exercises kill motivation.
5. **Provide progressive hints**: Don't show the solution immediately. Offer 3-4 hints that progressively reveal the answer, giving learners a chance to struggle productively.
6. **Measure and iterate**: Track completion rates and exercise pass rates. A step where >30% of learners fail or abandon needs rewording, not harder prerequisites.
7. **Support multiple languages**: When teaching concepts that apply across languages, provide code examples in at least the two most popular languages for your audience.
8. **Include knowledge checks**: Add brief quizzes between major sections to reinforce learning and help learners self-assess before moving on.
9. **Keep tutorials under 30 minutes**: Long tutorials lose attention. Split content into multiple focused tutorials, each completable in a single sitting.
10. **Update tutorials with the product**: When the underlying software changes, update tutorials immediately. Outdated tutorials erode trust faster than missing tutorials.

## Related Modules

- [documentation](../documentation/GROK.md) — General technical documentation authoring and lifecycle management
- [api-docs](../api-docs/GROK.md) — OpenAPI specification generation and API reference documentation
- [architecture-docs](../architecture-docs/GROK.md) — Architecture Decision Records and system design documentation
- [release-notes](../release-notes/GROK.md) — Automated release note generation and changelog management

## Advanced Configuration

### Assessment Engine Configuration

Customize assessment generation with a YAML configuration file:

```yaml
# tutorial-config.yml
assessment:
  question_types:
    - multiple_choice
    - code_completion
    - short_answer
    - fill_in_blank
  difficulty_distribution:
    easy: 0.3
    medium: 0.5
    hard: 0.2
  scoring:
    multiple_choice: 1
    code_completion: 3
    short_answer: 2
    fill_in_blank: 1
  passing_score: 70
  max_attempts: 3
  time_limit_minutes: 30
```

### Interactive Exercise Configuration

Configure the interactive exercise sandbox:

```yaml
exercises:
  sandbox:
    language: python
    version: "3.11"
    timeout_seconds: 30
    memory_limit_mb: 256
    allowed_modules: [math, collections, itertools, functools]
    blocked_modules: [os, sys, subprocess, socket]
  hints:
    reveal_strategy: progressive
    max_hints: 4
    penalty_per_hint: 0.1
    time_before_hint_seconds: 60
  validation:
    run_test_cases: true
    check_style: false
    require_docstring: false
```

### Analytics Configuration

```yaml
analytics:
  tracking:
    step_durations: true
    exercise_attempts: true
    hint_usage: true
    error_patterns: true
  reporting:
    generate_weekly: true
    retention_days: 365
    anonymize_data: true
  export:
    formats: [csv, json]
    include_pii: false
```

## Architecture Patterns

### Learning Path DAG

Learning paths are modeled as directed acyclic graphs (DAGs) where nodes are tutorials and edges are prerequisite relationships. The system validates that no cycles exist and that all prerequisites are satisfied:

```python
from tutorials import LearningPath, DAGValidator

path = LearningPath(id="python-backend", title="Python Backend Development")
# ... add modules and nodes ...

validator = DAGValidator(path)
if validator.has_cycles():
    print(f"Cyclic prerequisites detected: {validator.get_cycle()}")
else:
    print("Prerequisite graph is valid")
```

### Exercise Validation Pipeline

Exercise validation follows a pipeline pattern:

```
Student Submission -> Syntax Check -> Test Execution -> Result Aggregation -> Feedback
                       |               |                 |                    |
                   AST Parse       Sandboxed Run    Pass/Fail Count     Hint Generation
                   Type Check      Time Limits      Error Analysis      Solution Compare
```

### Multi-Language Content Architecture

Tutorials use a shared concept layer with language-specific code blocks:

```python
from tutorials import Tutorial, CodeBlock

tutorial = Tutorial(id="sorting-algorithms", title="Sorting Algorithms")

tutorial.add_concept(
    name="bubble_sort",
    explanation="Bubble sort repeatedly steps through the list...",
    code_blocks={
        "python": CodeBlock(language="python", code="def bubble_sort(arr):..."),
        "javascript": CodeBlock(language="javascript", code="function bubbleSort(arr) {...}"),
        "go": CodeBlock(language="go", code="func BubbleSort(arr []int) {...}"),
    }
)
```

## Integration Guide

### LMS Integration (SCORM)

Export tutorials as SCORM packages for Learning Management Systems:

```python
from tutorials import SCORMExporter, Tutorial

tutorial = Tutorial(id="intro-python", title="Introduction to Python")
# ... configure tutorial ...

exporter = SCORMExporter(tutorial)
exporter.export(
    output_path="intro-python-scorm.zip",
    manifest={
        "title": "Introduction to Python",
        "description": "Learn Python fundamentals",
        "version": "1.0",
        "mastery_score": 70,
    }
)
```

### CI/CD Pipeline Integration

```yaml
# .github/workflows/tutorial-check.yml
name: Tutorial Validation
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Prerequisites
        run: python -m tutorials.validate --check-prerequisites
      - name: Test Exercises
        run: python -m tutorials.test --exercises-dir exercises/
      - name: Check Analytics
        run: python -m tutorials.analytics --check-completion-rates
```

### Webhook Integration

```python
from tutorials import TutorialAnalytics, WebhookNotifier

analytics = TutorialAnalytics(data_dir="analytics/")
notifier = WebhookNotifier(webhook_url="https://hooks.slack.com/services/xxx")

# Notify when completion rate drops
report = analytics.analyze("intro-python")
if report.completion_rate < 0.5:
    notifier.send(
        channel="#tutorial-alerts",
        message=f"Low completion rate for intro-python: {report.completion_rate:.1%}"
    )
```

## Performance Optimization

### Caching Assessment Results

Cache generated assessments to avoid regeneration:

```python
from tutorials import AssessmentEngine, CacheConfig

engine = AssessmentEngine(
    tutorials=["intro-python"],
    cache_config=CacheConfig(
        enabled=True,
        cache_dir=".assessment-cache/",
        ttl_seconds=3600
    )
)
```

### Parallel Exercise Validation

Validate multiple submissions concurrently:

```python
from tutorials import InteractiveExercise, ParallelConfig

exercise = InteractiveExercise(
    id="sorting-exercise",
    parallel_config=ParallelConfig(enabled=True, workers=4)
)

# Validates multiple submissions in parallel
results = exercise.validate_batch(submissions)
```

### Analytics Data Aggregation

Pre-aggregate analytics data for faster reporting:

```python
from tutorials import TutorialAnalytics, AggregationConfig

analytics = TutorialAnalytics(
    data_dir="analytics/",
    aggregation_config=AggregationConfig(
        enable_pre_aggregation=True,
        aggregation_interval="daily",
        retention_days=365
    )
)
```

## Security Considerations

### Code Submission Security

Validate and sandbox all student code submissions:

```python
from tutorials import SecurityConfig, InteractiveExercise

exercise = InteractiveExercise(
    id="code-exercise",
    security_config=SecurityConfig(
        sandbox_enabled=True,
        max_execution_time_seconds=10,
        max_memory_mb=128,
        blocked_builtins=["exec", "eval", "compile", "__import__"],
        network_access=False,
        file_system_access=False
    )
)
```

### Assessment Integrity

Protect assessment content from tampering:

```python
from tutorials import AssessmentEngine, IntegrityConfig

engine = AssessmentEngine(
    integrity_config=IntegrityConfig(
        shuffle_questions=True,
        shuffle_options=True,
        randomize_values=True,
        hash_answers=True
    )
)
```

### Data Privacy

Ensure learner data privacy compliance:

```python
from tutorials import PrivacyConfig

config = PrivacyConfig(
    anonymize_analytics=True,
    retention_days=365,
    export_requires_consent=True,
    delete_on_request=True
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Prerequisite cycle detected | Circular dependency in learning path | Use `DAGValidator.get_cycle()` to find and break the cycle |
| Exercise validator fails | Incorrect validator function | Ensure validator returns boolean, check test case inputs |
| Assessment generation slow | Too many tutorials loaded | Reduce tutorial scope or enable caching |
| Analytics data missing | Tracking not enabled | Verify analytics configuration and tracking flags |
| Multi-language rendering fails | Missing language template | Add code block for the missing language |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from tutorials import Tutorial, InteractiveExercise

tutorial = Tutorial(id="debug-tutorial", debug=True)
# Verbose output for all operations
```

### Log Output

```
[DEBUG] tutorials.prerequisites: Validating 12 prerequisite relationships
[DEBUG] tutorials.exercise: Running 5 test cases for exercise list-comprehension
[WARNING] tutorials.analytics: Low completion rate (42%) for step 3
[ERROR] tutorials.assessment: Question q7 has no correct answer defined
[INFO] tutorials.tutorial: Tutorial intro-python completed in 28 minutes
```

## API Reference

### Tutorial

```python
class Tutorial:
    def __init__(self, id: str, title: str, difficulty: str = "beginner",
                 estimated_minutes: int = 30,
                 learning_objectives: List[str] = None):
        """Initialize a tutorial."""

    def add_step(self, step: TutorialStep) -> None:
        """Add a step to the tutorial."""

    def to_markdown(self) -> str:
        """Render tutorial as Markdown."""

    def validate(self) -> List[str]:
        """Validate tutorial structure and prerequisites."""
```

### InteractiveExercise

```python
class InteractiveExercise:
    def __init__(self, id: str, title: str, language: str,
                 problem: str, starter_code: str,
                 test_cases: List[dict] = None,
                 hints: List[HintLevel] = None,
                 security_config: SecurityConfig = None):
        """Initialize an interactive exercise."""

    def validate(self, submission: str) -> ExerciseResult:
        """Validate a student submission against test cases."""

    def validate_batch(self, submissions: List[str]) -> List[ExerciseResult]:
        """Validate multiple submissions in parallel."""
```

### AssessmentEngine

```python
class AssessmentEngine:
    def __init__(self, tutorials: List[str],
                 question_types: List[QuestionType] = None,
                 difficulty_distribution: Dict[str, float] = None,
                 integrity_config: IntegrityConfig = None):
        """Initialize the assessment engine."""

    def generate(self, num_questions: int) -> Assessment:
        """Generate an assessment from tutorial content."""

    def score(self, assessment: Assessment, submission: dict) -> Score:
        """Score a student submission."""
```

## Data Models

### Tutorial

```python
@dataclass
class Tutorial:
    id: str
    title: str
    difficulty: str  # beginner, intermediate, advanced
    estimated_minutes: int
    learning_objectives: List[str]
    steps: List[TutorialStep]
    prerequisites: List[str]
    metadata: Dict[str, Any]
```

### LearningPath

```python
@dataclass
class LearningPath:
    id: str
    title: str
    description: str
    modules: List[LearningModule]
    total_minutes: int
    difficulty_progression: List[str]
    skill_nodes: List[SkillNode]
```

### ExerciseResult

```python
@dataclass
class ExerciseResult:
    passed: bool
    tests_passed: int
    tests_total: int
    execution_time_ms: int
    memory_used_mb: float
    feedback: List[str]
    hints_used: int
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "tutorials.server", "--host", "0.0.0.0", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tutorial-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tutorials
  template:
    spec:
      containers:
        - name: tutorials
          image: tutorials:latest
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 2000m
              memory: 2Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from tutorials import MetricsCollector

metrics = MetricsCollector(prefix="tutorials")

# Track tutorial metrics
metrics.histogram("tutorial_completion_minutes", minutes, labels={"tutorial_id": tid})
metrics.counter("tutorial_completions_total", count, labels={"tutorial_id": tid})
metrics.gauge("exercise_pass_rate", rate, labels={"exercise_id": eid})
```

### Alerting Rules

```yaml
groups:
  - name: tutorials
    rules:
      - alert: LowCompletionRate
        expr: tutorials_completion_rate < 0.5
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "Tutorial completion rate below 50%"

      - alert: HighExerciseFailureRate
        expr: tutorials_exercise_failure_rate > 0.7
        for: 3d
        labels:
          severity: critical
        annotations:
          summary: "Exercise failure rate above 70%"
```

## Testing Strategy

### Unit Tests

```python
def test_tutorial_step_prerequisites():
    step = TutorialStep(order=2, prerequisites=["intro-python-basics"])
    assert step.prerequisites == ["intro-python-basics"]

def test_exercise_validation():
    exercise = InteractiveExercise(
        id="test", title="Test", language="python",
        problem="Return 42", starter_code="def answer(): pass",
        test_cases=[{"input": None, "expected": 42}]
    )
    result = exercise.validate("def answer(): return 42")
    assert result.passed
```

### Integration Tests

```python
def test_learning_path_validation():
    path = LearningPath(id="test-path", title="Test Path")
    # ... add nodes with prerequisites ...
    issues = path.validate()
    assert len(issues) == 0
```

## Versioning & Migration

### Semantic Versioning

The tutorials module follows semantic versioning:
- **Major**: Breaking changes to public API or exercise format
- **Minor**: New features, new assessment types, new analytics
- **Patch**: Bug fixes, improved validation

### Deprecation Policy

Deprecated features receive warnings for one minor version before removal. Migration guides are provided for all breaking changes.

## Glossary

| Term | Definition |
|------|-----------|
| **Tutorial** | A structured learning experience with step-by-step instructions and exercises |
| **Learning Path** | An ordered sequence of tutorials with prerequisite relationships |
| **Prerequisite** | A tutorial that must be completed before starting another |
| **Exercise** | A hands-on coding challenge embedded within a tutorial |
| **Assessment** | A quiz or test generated from tutorial content |
| **Skill Tree** | A visual representation of tutorial progress and skill acquisition |
| **Hint Level** | A progressive hint system that reveals solutions gradually |
| **Completion Rate** | The percentage of learners who finish a tutorial |

## Changelog

### v1.4.0 (Latest)
- Added analytics dashboard with effectiveness metrics
- Added multi-language support for code examples
- Improved assessment generation quality

### v1.3.0
- Added skill tree visualization
- Added interactive exercise validation
- Improved prerequisite graph validation

### v1.2.0
- Added assessment generation engine
- Added progressive hint system
- Improved exercise test case execution

### v1.1.0
- Added interactive coding exercises
- Added prerequisite tracking
- Improved tutorial template system

### v1.0.0
- Initial release with tutorial authoring
- Learning path design
- Multi-language support
- Effectiveness analytics

## Contributing Guidelines

### How to Contribute

1. Fork the repository and create a feature branch
2. Follow existing code style and patterns
3. Write tests for new features
4. Update documentation as needed
5. Ensure all CI checks pass
6. Submit a pull request with a clear description

### Adding New Tutorial Types

1. Create a new template class extending `TutorialBase`
2. Implement required methods: `to_markdown()`, `validate()`
3. Add to the template registry
4. Write tests for the new type
5. Update documentation

## License

MIT License

Copyright (c) 2025 Example Organization

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

### Dependencies

- `markdown` >= 3.5 — Markdown rendering for tutorials
- `pyyaml` >= 6.0 — Configuration parsing
- `mermaid-py` >= 0.3 — Skill tree diagram generation
- `pytest` >= 7.0 — Exercise test case execution
- `statistics` >= 1.0 — Analytics calculations

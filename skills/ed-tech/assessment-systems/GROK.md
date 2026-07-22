---
name: "Assessment Systems"
version: "2.0.0"
description: "Comprehensive assessment systems toolkit with question banks, auto-grading, rubric-based evaluation, proctoring integration, and analytics for educational assessment"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ed-tech", "assessment", "question-banks", "auto-grading", "rubrics", "proctoring"]
category: "ed-tech"
personality: "assessment-engineer"
use_cases: ["question banks", "auto-grading", "rubric evaluation", "proctoring", "assessment analytics"]
---

# Assessment Systems

> Production-grade assessment framework providing question bank management, auto-grading, rubric-based evaluation, proctoring integration, and comprehensive assessment analytics for educational technology.

## Overview

The Assessment Systems module provides tools for creating, delivering, and grading assessments. It implements question bank management with item analysis, automated grading for multiple question types, rubric-based evaluation for subjective assessments, integration with proctoring services, and detailed assessment analytics. Every feature includes accessibility support and anti-cheating measures.

## Core Capabilities

### 1. Question Bank Management
- Multiple question types (MCQ, T/F, short answer, essay, code)
- Question tagging and categorization
- Item difficulty and discrimination analysis
- Version control for questions
- Randomized question selection

### 2. Auto-Grading
- MCQ and T/F auto-grading
- Pattern matching for short answers
- Code execution and testing
- Rubric-based essay scoring
- Partial credit calculation

### 3. Rubric Evaluation
- Analytic and holistic rubrics
- Criteria-based scoring
- Inter-rater reliability tracking
- Rubric templates
- Calibrated grading sessions

### 4. Proctoring Integration
- Browser lockdown integration
- Webcam monitoring
- Screen recording
- Identity verification
- Anomaly detection

### 5. Assessment Analytics
- Item analysis (difficulty, discrimination)
- Test reliability calculation
- Score distribution analysis
- Distractor analysis
- Assessment validity metrics

### 6. Anti-Cheating
- Question randomization
- Answer option shuffling
- Time limit enforcement
- Plagiarism detection
- IP monitoring

## Usage Examples

### Question Bank

```python
from assessment_systems import QuestionBank, Question, QuestionType

bank = QuestionBank()

# Add questions
bank.add_question(Question(
    id="q1",
    type=QuestionType.MCQ,
    text="What is the capital of France?",
    options=["London", "Berlin", "Paris", "Madrid"],
    correct_answer="Paris",
    difficulty=0.3,
    tags=["geography", "europe"],
))

# Get random questions
questions = bank.get_random(n=10, tags=["geography"], difficulty_range=(0.2, 0.8))
print(f"Selected {len(questions)} questions")
```

### Auto-Grading

```python
from assessment_systems import AutoGrader

grader = AutoGrader()

# Grade MCQ
result = grader.grade_mcq(
    question_id="q1",
    student_answer="Paris",
    correct_answer="Paris",
)
print(f"Score: {result.points}/{result.max_points}")

# Grade code submission
code_result = grader.grade_code(
    question_id="q5",
    student_code="def add(a, b): return a + b",
    test_cases=[{"input": [1, 2], "expected": 3}],
)
print(f"Tests passed: {code_result.tests_passed}/{code_result.tests_total}")
```

### Rubric Evaluation

```python
from assessment_systems import RubricEvaluator, Rubric

evaluator = RubricEvaluator()

# Create rubric
rubric = Rubric(
    name="Essay Grading",
    criteria=[
        {"name": "Thesis", "max_points": 25, "levels": ["Clear", "Somewhat clear", "Unclear"]},
        {"name": "Evidence", "max_points": 25, "levels": ["Strong", "Adequate", "Weak"]},
        {"name": "Organization", "max_points": 25, "levels": ["Excellent", "Good", "Poor"]},
        {"name": "Mechanics", "max_points": 25, "levels": ["Excellent", "Good", "Poor"]},
    ],
)

# Grade essay
result = evaluator.grade(
    rubric=rubric,
    submission="Essay text here...",
    scores={"Thesis": 20, "Evidence": 18, "Organization": 22, "Mechanics": 23},
)
print(f"Total: {result.total_points}/{result.max_points}")
print(f"Grade: {result.grade}")
```

### Assessment Analytics

```python
from assessment_systems import AssessmentAnalytics

analytics = AssessmentAnalytics()

# Analyze assessment
report = analytics.analyze(assessment_id="quiz-1")
print(f"Mean: {report.mean:.1f}")
print(f"Std Dev: {report.std_dev:.1f}")
print(f"Reliability: {report.reliability:.3f}")
print(f"Items analyzed: {report.item_count}")

print("\nItem analysis:")
for item in report.items[:5]:
    print(f"  {item.question_id}: difficulty={item.difficulty:.2f}, discrimination={item.discrimination:.2f}")
```

## Best Practices

### Question Design
- Write clear, unambiguous questions
- Include plausible distractors for MCQ
- Avoid negative phrasing when possible
- Test at multiple cognitive levels

### Auto-Grading
- Validate auto-graded results periodically
- Provide detailed feedback for incorrect answers
- Handle edge cases in code grading
- Use partial credit generously

### Rubrics
- Define clear criteria and levels
- Calibrate graders before grading
- Track inter-rater reliability
- Provide exemplars for each level

### Anti-Cheating
- Combine multiple anti-cheating measures
- Focus on detection, not prevention
- Handle accusations professionally
- Use honor codes alongside technical measures

## Related Modules

- **learning-platforms**: Platform integration for assessments
- **adaptive-learning**: Adaptive assessment delivery
- **student-analytics**: Assessment performance analytics
- **content-delivery**: Content delivery for assessments

---

## Advanced Configuration

### Question Bank Settings

```python
from assessment_systems import QuestionBankConfig

config = QuestionBankConfig(
    # Randomization
    randomization_method="stratified",
    seed_increment_per_session=True,
    
    # Difficulty Distribution
    difficulty_distribution={
        "easy": 0.3,
        "medium": 0.5,
        "hard": 0.2,
    },
    
    # Item Pool
    item_pool_size=5000,
    refresh_rate_days=30,
    deactivation_threshold=0.3,  # discrimination index
    
    # Anti-Cheating
    answer_shuffling=True,
    question_shuffling=True,
    time_limit_enforcement=True,
    max_attempts_per_question=3,
)
```

### Auto-Grading Configuration

```python
from assessment_systems import GradingConfig

grading_config = GradingConfig(
    # Code Grading
    code_grading={
        "timeout_seconds": 30,
        "max_memory_mb": 256,
        "sandbox_type": "docker",
        "allowed_languages": ["python", "javascript", "java"],
        "test_case_limit": 50,
    },
    
    # Essay Grading
    essay_grading={
        "min_words": 100,
        "max_words": 2000,
        "grammar_check": True,
        "plagiarism_check": True,
        "ai_detection": True,
    },
    
    # Partial Credit
    partial_credit_enabled=True,
    partial_credit_method="proportional",
    minimum_score_for_partial=0.5,
)
```

## Architecture Patterns

### Assessment Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Content   │────▶│   Item       │────▶│  Quality    │
│   Creation  │     │   Review     │     │  Control    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                                                ▼
┌─────────────────┐     ┌─────────────────────────┐
│  Bank Storage   │◀────│  Approval                │
└────────┬────────┘     └─────────────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│  Assessment    │────▶│  Delivery   │
│  Assembly      │     │             │
└─────────────────┘     └──────┬──────┘
                               │
                               ▼
┌─────────────────┐     ┌─────────────┐
│  Auto-Grade     │◀────│  Submission │
└────────┬────────┘     └─────────────┘
         │
         ▼
┌─────────────────┐
│  Results &      │
│  Analytics      │
└─────────────────┘
```

### Item Response Theory Integration

```python
from assessment_systems import IRTAnalyzer

irt = IRTAnalyzer()

# Estimate item parameters
params = irt.estimate_item_parameters(
    response_matrix=responses,
    model="3PL",  # 3-parameter logistic
)

print(f"Items estimated: {len(params)}")
for item in params[:5]:
    print(f"  {item.id}: a={item.discrimination:.2f}, b={item.difficulty:.2f}, c={item.guessing:.2f}")

# Estimate ability
abilities = irt.estimate_ability(
    response_matrix=responses,
    item_params=params,
)

print(f"Learners estimated: {len(abilities)}")
```

## Integration Guide

### LMS Integration

```python
from assessment_systems import LMSIntegration

lms = LMSIntegration(provider="canvas")

# Import questions from LMS
questions = lms.import_questions(
    course_id="course-123",
    question_type="all",
    format="qti",
)

# Export results to LMS
lms.export_grades(
    assessment_id="quiz-101",
    grades=[
        {"learner_id": "user-1", "score": 85, "passed": True},
        {"learner_id": "user-2", "score": 72, "passed": True},
    ],
)
```

### Proctoring Service Integration

```python
from assessment_systems import ProctoringService

proctoring = ProctoringService(provider="respondus")

# Start proctored session
session = proctoring.start_session(
    assessment_id="exam-101",
    learner_id="student@example.com",
    settings={
        "webcam_required": True,
        "screen_recording": True,
        "browser_lockdown": True,
        "identity_verification": True,
    },
)

print(f"Session ID: {session.id}")
print(f"Proctoring URL: {session.proctoring_url}")

# Get session report
report = proctoring.get_report(session.id)
print(f"Flagged events: {len(report.flagged_events)}")
for event in report.flagged_events:
    print(f"  {event.timestamp}: {event.type} - {event.severity}")
```

## Performance Optimization

### Question Pool Optimization

```python
from assessment_systems import PoolOptimizer

optimizer = PoolOptimizer()

# Optimize question pool
optimized = optimizer.optimize(
    pool_id="algebra-pool",
    target_metrics={
        "avg_difficulty": 0.5,
        "avg_discrimination": 0.7,
        "coverage": 0.9,
    },
)

print(f"Questions removed: {optimized.removed_count}")
print(f"Questions added: {optimized.added_count}")
print(f"Pool quality score: {optimized.quality_score:.2f}")
```

### Parallel Grading

```python
from assessment_systems import ParallelGrader

grader = ParallelGrader(workers=8)

# Grade submissions in parallel
results = grader.grade_batch(
    assessment_id="quiz-101",
    submissions=submissions,
    grading_method="auto",
    timeout_seconds=60,
)

print(f"Graded: {results.completed}/{results.total}")
print(f"Average time per submission: {results.avg_time_ms:.0f}ms")
```

## Security Considerations

### Anti-Cheating Measures

```python
from assessment_systems import AntiCheat

anti_cheat = AntiCheat()

# Analyze submission for cheating indicators
analysis = anti_cheat.analyze_submission(
    submission_id="sub-101",
    checks=[
        "timing_analysis",
        "copy_paste_detection",
        "tab_switching",
        "ip_consistency",
        "answer_similarity",
    ],
)

print(f"Risk score: {analysis.risk_score:.2f}")
print(f"Flagged indicators: {analysis.flagged_indicators}")
```

### Question Security

```python
from assessment_systems import QuestionSecurity

security = QuestionSecurity()

# Encrypt questions at rest
encrypted = security.encrypt_bank(
    bank_id="exam-questions",
    encryption_key="aes-256-key",
)

# Secure delivery
secure_url = security.generate_secure_url(
    question_id="q-123",
    expiry_minutes=30,
    ip_restrictions=["192.168.1.0/24"],
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow auto-grading | Large test cases | Optimize test cases, increase workers |
| Duplicate submissions | Race condition | Implement idempotency keys |
| Proctoring errors | Browser compatibility | Update browser requirements |
| Low discrimination | Poor questions | Remove/revamp low-discrimination items |
| Grade sync issues | API timeout | Implement retry logic |

### Debug Mode

```python
from assessment_systems import enable_debug

enable_debug(
    components=["grading", "proctoring", "analytics"],
    log_level="DEBUG",
)

# Debug grading
debug_result = debug.trace_grading(
    submission_id="sub-101",
    verbose=True,
)
```

## API Reference

### REST Endpoints

```
GET    /api/v1/question-banks                 List question banks
POST   /api/v1/question-banks                 Create question bank
GET    /api/v1/question-banks/{id}/questions   List questions
POST   /api/v1/question-banks/{id}/questions   Add questions

POST   /api/v1/assessments                    Create assessment
GET    /api/v1/assessments/{id}               Get assessment
POST   /api/v1/assessments/{id}/start         Start assessment
POST   /api/v1/assessments/{id}/submit        Submit assessment

GET    /api/v1/submissions/{id}/grade         Get grade
POST   /api/v1/submissions/{id}/grade         Update grade
GET    /api/v1/submissions/{id}/feedback      Get feedback
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class QuestionType(Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODE = "code"
    FILE_UPLOAD = "file_upload"

@dataclass
class Question:
    id: UUID
    bank_id: UUID
    type: QuestionType
    text: str
    options: Optional[List[str]]
    correct_answer: str
    difficulty: float
    discrimination: float
    tags: List[str]
    created_at: datetime

@dataclass
class Assessment:
    id: UUID
    title: str
    course_id: UUID
    questions: List[Question]
    time_limit_minutes: int
    passing_score: float
    max_attempts: int
    proctoring_enabled: bool
    created_at: datetime

@dataclass
class Submission:
    id: UUID
    assessment_id: UUID
    learner_id: UUID
    answers: dict
    score: Optional[float]
    passed: Optional[bool]
    started_at: datetime
    submitted_at: Optional[datetime]

@dataclass
class GradingResult:
    submission_id: UUID
    total_score: float
    max_score: float
    percentage: float
    passed: bool
    question_scores: List["QuestionScore"]
    feedback: str
    graded_at: datetime
```

## Deployment Guide

### Docker Configuration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for code grading
RUN apt-get update && apt-get install -y \
    gcc g++ make \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create sandbox for code execution
RUN mkdir -p /sandbox

EXPOSE 8000
CMD ["uvicorn", "assessment_systems.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring & Observability

### Key Metrics

```python
from assessment_systems import Metrics

metrics = Metrics()

# Track grading performance
metrics.histogram("grading.duration_ms", duration, tags={"type": "auto"})
metrics.counter("grading.submissions_total", tags={"status": "success"})

# Track question performance
metrics.gauge("question.avg_difficulty", difficulty, tags={"bank": "algebra"})
metrics.gauge("question.avg_discrimination", discrimination, tags={"bank": "algebra"})

# Track proctoring
metrics.counter("proctoring.flagged_events", tags={"severity": "high"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from assessment_systems import AutoGrader, QuestionBank

@pytest.fixture
def grader():
    return AutoGrader(test_mode=True)

def test_grade_mcq(grader):
    result = grader.grade_mcq(
        question_id="q1",
        student_answer="Paris",
        correct_answer="Paris",
    )
    assert result.points == result.max_points

def test_grade_code(grader):
    result = grader.grade_code(
        question_id="q5",
        student_code="def add(a, b): return a + b",
        test_cases=[
            {"input": [1, 2], "expected": 3},
            {"input": [0, 0], "expected": 0},
        ],
    )
    assert result.tests_passed == 2
```

## Versioning & Migration

### Version History

- **2.0.0**: Added IRT analysis, advanced proctoring, parallel grading
- **1.5.0**: Added code grading, plagiarism detection
- **1.0.0**: Initial release with MCQ and essay grading

## Glossary

| Term | Definition |
|------|------------|
| **IRT** | Item Response Theory |
| **Discrimination** | Ability of item to differentiate between high and low performers |
| **Difficulty** | Proportion of correct responses |
| **Distractor** | Incorrect option in MCQ |
| **Rubric** | Scoring guide for subjective items |
| **Formative** | Assessment during learning |
| **Summative** | Assessment of learning |

## Changelog

### Version 2.0.0
- IRT integration for item analysis
- Advanced proctoring features
- Parallel grading engine
- Improved code grading sandbox

### Version 1.5.0
- Code execution grading
- Plagiarism detection
- Enhanced rubric tools

### Version 1.0.0
- Initial release
- MCQ and essay grading
- Basic question bank

## Contributing Guidelines

1. Follow security best practices
2. Test grading edge cases
3. Document API changes
4. Validate with real assessments

## Assessment System Architecture

### Computerized Adaptive Testing (CAT)

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class ItemType(Enum):
    MULTIPLE_CHOICE = "mcq"
    TRUE_FALSE = "tf"
    SHORT_ANSWER = "sa"
    ESSAY = "essay"
    DRAG_DROP = "drag"
    CODE = "code"

@dataclass
class ItemParameters:
    item_id: str
    item_type: ItemType
    discrimination: float
    difficulty: float
    guessing: float
    skill_ids: List[str]
    content: Dict
    metadata: Dict = field(default_factory=dict)

class IRTModel:
    @staticmethod
    def probability_3pl(theta: float, a: float, b: float, c: float) -> float:
        exponent = -a * (theta - b)
        return c + (1 - c) / (1 + np.exp(exponent))
    
    @staticmethod
    def expected_information(theta: float, a: float, b: float, c: float) -> float:
        p = IRTModel.probability_3pl(theta, a, b, c)
        q = 1 - p
        if p <= 0 or p >= 1:
            return 0.0
        numerator = (a ** 2) * ((p - c) ** 2)
        denominator = ((1 - c) ** 2) * p * q
        return numerator / denominator if denominator > 0 else 0.0

class ComputerizedAdaptiveTest:
    def __init__(self, items: List[ItemParameters], max_items: int = 30, 
                 min_items: int = 5, info_threshold: float = 0.5):
        self.item_bank = items
        self.max_items = max_items
        self.min_items = min_items
        self.info_threshold = info_threshold
        self.theta = 0.0
        self.theta_se = 1.0
        self.administered: List[Tuple[ItemParameters, bool]] = []
        self.available = list(items)
    
    def select_next_item(self) -> Optional[ItemParameters]:
        if not self.available:
            return None
        best_item = None
        best_info = -1
        for item in self.available:
            info = IRTModel.expected_information(
                self.theta, item.discrimination, item.difficulty, item.guessing)
            exposure_rate = item.metadata.get("exposure_rate", 0.0)
            adjusted_info = info * (1.0 - 0.3 * exposure_rate)
            if adjusted_info > best_info:
                best_info = adjusted_info
                best_item = item
        return best_item
    
    def record_response(self, item: ItemParameters, response: str, correct: bool,
                       response_time_ms: float):
        self.administered.append((item, correct))
        self.available = [i for i in self.available if i.item_id != item.item_id]
        self._update_ability()
        item.metadata["exposure_rate"] = item.metadata.get("exposure_rate", 0.0) + 1.0
    
    def _update_ability(self):
        theta = self.theta
        for _ in range(20):
            log_l_first = 0.0
            log_l_second = 0.0
            for item, correct in self.administered:
                p = IRTModel.probability_3pl(theta, item.discrimination, item.difficulty, item.guessing)
                q = 1 - p
                if p <= 0 or p >= 1:
                    continue
                if correct:
                    log_l_first += item.discrimination * (p - item.guessing) / (p * (1 - item.guessing))
                else:
                    log_l_first -= item.discrimination * (1 - p) / q
                log_l_second -= (item.discrimination ** 2) * p * q
            if abs(log_l_second) < 1e-10:
                break
            theta -= log_l_first / log_l_second
        self.theta = np.clip(theta, -4, 4)
        total_info = sum(
            IRTModel.expected_information(self.theta, i.discrimination, i.difficulty, i.guessing)
            for i, _ in self.administered
        )
        self.theta_se = 1.0 / np.sqrt(total_info) if total_info > 0 else 1.0
    
    def is_complete(self) -> bool:
        if len(self.administered) >= self.max_items:
            return True
        if len(self.administered) >= self.min_items and self.theta_se < self.info_threshold:
            return True
        return False
    
    def get_results(self) -> Dict:
        return {
            "theta": round(self.theta, 3),
            "standard_error": round(self.theta_se, 3),
            "items_administered": len(self.administered),
            "ability_level": self._ability_to_level(),
            "confidence_interval": (
                round(self.theta - 1.96 * self.theta_se, 3),
                round(self.theta + 1.96 * self.theta_se, 3),
            ),
        }
    
    def _ability_to_level(self) -> str:
        if self.theta < -2: return "Below Basic"
        elif self.theta < -0.5: return "Basic"
        elif self.theta < 1.0: return "Proficient"
        elif self.theta < 2.0: return "Advanced"
        return "Exemplary"

class TestSecurityManager:
    def __init__(self):
        self.item_exposure: Dict[str, int] = {}
    
    def check_collusion(self, responses_a: List[Tuple[str, bool]], 
                       responses_b: List[Tuple[str, bool]]) -> float:
        common = set(r[0] for r in responses_a) & set(r[0] for r in responses_b)
        if len(common) < 5:
            return 0.0
        a_dict = dict(responses_a)
        b_dict = dict(responses_b)
        agreements = sum(1 for item_id in common if a_dict[item_id] == b_dict[item_id])
        return agreements / len(common)
    
    def detect_speeding(self, responses: List[Dict], time_limit_ms: int = 1000) -> List[str]:
        return [r["item_id"] for r in responses 
                if r.get("response_time_ms", float('inf')) < time_limit_ms]

class EssayScorer:
    def __init__(self):
        self.rubric_weights = {
            "thesis": 0.20, "evidence": 0.25, "analysis": 0.25,
            "organization": 0.15, "mechanics": 0.15,
        }
    
    def score(self, essay_text: str) -> Dict:
        word_count = len(essay_text.split())
        sentences = [s.strip() for s in essay_text.split('.') if s.strip()]
        paragraphs = essay_text.split('\n\n')
        
        scores = {}
        scores["thesis"] = {"score": min(10, 5 + self._detect_thesis_strength(essay_text)),
                           "weight": self.rubric_weights["thesis"]}
        scores["evidence"] = {"score": min(10, 3 + self._count_evidence_markers(essay_text)),
                             "weight": self.rubric_weights["evidence"]}
        scores["analysis"] = {"score": min(10, 2 + self._measure_analytical_depth(essay_text)),
                             "weight": self.rubric_weights["analysis"]}
        scores["organization"] = {"score": min(10, 3 + len(paragraphs)),
                                 "weight": self.rubric_weights["organization"]}
        scores["mechanics"] = {"score": min(10, 5 + self._grammar_score(essay_text)),
                              "weight": self.rubric_weights["mechanics"]}
        
        weighted_total = sum(s["score"] * s["weight"] for s in scores.values())
        return {
            "scores": scores, "weighted_total": round(weighted_total, 2),
            "word_count": word_count, "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "readability": self._flesch_kincaid(essay_text),
            "feedback": self._generate_feedback(scores),
        }
    
    def _detect_thesis_strength(self, text: str) -> float:
        indicators = ["clearly states", "argues that", "contends"]
        return min(5.0, sum(2.0 for ind in indicators if ind.lower() in text.lower()))
    
    def _count_evidence_markers(self, text: str) -> float:
        indicators = ["according to", "research shows", "studies indicate"]
        return min(7.0, sum(2.0 for ind in indicators if ind.lower() in text.lower()))
    
    def _measure_analytical_depth(self, text: str) -> float:
        import re
        matches = len(re.findall(r"therefore|thus|consequently|this suggests", text, re.IGNORECASE))
        return min(8.0, matches * 1.5)
    
    def _grammar_score(self, text: str) -> float:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        avg_words = np.mean([len(s.split()) for s in sentences]) if sentences else 0
        return 5.0 - (1.0 if avg_words > 40 else 0) - (2.0 if avg_words < 5 else 0)
    
    def _flesch_kincaid(self, text: str) -> float:
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        syllables = sum(max(1, len([c for c in w.lower() if c in "aeiouy"])) for w in words)
        if not sentences or not words:
            return 0.0
        return 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
    
    def _generate_feedback(self, scores: Dict) -> List[str]:
        feedback = []
        for component, data in scores.items():
            if data["score"] < 5:
                feedback.append(f"Needs improvement in {component}")
            elif data["score"] >= 8:
                feedback.append(f"Excellent {component} work")
        return feedback
```

### Item Analysis and Test Statistics

```python
class ItemAnalyzer:
    def __init__(self):
        self.response_data: Dict[str, List[Dict]] = {}
    
    def record_response(self, item_id: str, learner_ability: float, correct: bool,
                       response_time_ms: float):
        self.response_data.setdefault(item_id, []).append({
            "ability": learner_ability, "correct": correct,
            "response_time_ms": response_time_ms,
        })
    
    def compute_item_statistics(self, item_id: str) -> Dict:
        responses = self.response_data.get(item_id, [])
        if len(responses) < 10:
            return {"item_id": item_id, "insufficient_data": True}
        
        correct_count = sum(1 for r in responses if r["correct"])
        p_value = correct_count / len(responses)
        
        abilities = [r["ability"] for r in responses]
        correct_abilities = [r["ability"] for r in responses if r["correct"]]
        incorrect_abilities = [r["ability"] for r in responses if not r["correct"]]
        
        point_biserial = self._point_biserial(
            [1 if r["correct"] else 0 for r in responses], abilities)
        
        avg_time = np.mean([r["response_time_ms"] for r in responses])
        avg_time_correct = np.mean([r["response_time_ms"] for r in responses if r["correct"]]) if correct_abilities else 0
        avg_time_incorrect = np.mean([r["response_time_ms"] for r in responses if not r["correct"]]) if incorrect_abilities else 0
        
        return {
            "item_id": item_id,
            "p_value": round(p_value, 3),
            "point_biserial": round(point_biserial, 3),
            "discrimination": "high" if point_biserial > 0.3 else "moderate" if point_biserial > 0.15 else "low",
            "avg_response_time_ms": round(avg_time, 0),
            "time_differential_ms": round(avg_time_correct - avg_time_incorrect, 0),
            "n_responses": len(responses),
            "recommendation": self._recommend(p_value, point_biserial),
        }
    
    def _point_biserial(self, scores: List[int], abilities: List[float]) -> float:
        n = len(scores)
        if n < 2:
            return 0.0
        mean_score = np.mean(scores)
        mean_ability = np.mean(abilities)
        std_ability = np.std(abilities, ddof=1)
        if std_ability == 0:
            return 0.0
        cov = np.sum((np.array(scores) - mean_score) * (np.array(abilities) - mean_ability)) / (n - 1)
        return cov / (std_ability * np.std(scores, ddof=1)) if np.std(scores, ddof=1) > 0 else 0.0
    
    def _recommend(self, p_value: float, point_biserial: float) -> str:
        if p_value < 0.2:
            return "Too difficult - review content or simplify"
        elif p_value > 0.9:
            return "Too easy - increase difficulty"
        elif point_biserial < 0.15:
            return "Poor discrimination - revise or replace"
        elif point_biserial > 0.4:
            return "Excellent item - retain in bank"
        return "Acceptable - monitor over time"
    
    def compute_test_reliability(self) -> float:
        all_items = list(self.response_data.keys())
        if len(all_items) < 5:
            return 0.0
        item_variances = []
        for item_id in all_items:
            responses = self.response_data[item_id]
            scores = [1 if r["correct"] else 0 for r in responses]
            item_variances.append(np.var(scores))
        total_variance = np.var([sum(1 for r in responses if r["correct"]) 
                                for responses in [self.response_data[i] for i in all_items[:5]]])
        if total_variance == 0:
            return 0.0
        return min(0.95, 1 - sum(item_variances) / (len(all_items) * total_variance))

class TestFormBuilder:
    def __init__(self, item_bank: List[ItemParameters]):
        self.item_bank = item_bank
    
    def build_parallel_forms(self, n_forms: int, items_per_form: int) -> List[List[ItemParameters]]:
        forms = [[] for _ in range(n_forms)]
        for item in sorted(self.item_bank, key=lambda x: x.difficulty):
            min_form = min(range(n_forms), key=lambda i: len(forms[i]))
            forms[min_form].append(item)
        
        return [form[:items_per_form] for form in forms]
    
    def equate_forms(self, form_a_scores: List[float], form_b_scores: List[float]) -> Dict:
        mean_a, mean_b = np.mean(form_a_scores), np.mean(form_b_scores)
        std_a, std_b = np.std(form_a_scores), np.std(form_b_scores)
        
        linear_equating = {
            "slope": std_b / std_a if std_a > 0 else 1.0,
            "intercept": mean_b - (std_b / std_a) * mean_a if std_a > 0 else 0,
        }
        
        return {
            "method": "linear",
            "parameters": linear_equating,
            "form_a_stats": {"mean": round(mean_a, 2), "std": round(std_a, 2), "n": len(form_a_scores)},
            "form_b_stats": {"mean": round(mean_b, 2), "std": round(std_b, 2), "n": len(form_b_scores)},
        }
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
---
name: "Adaptive Learning"
version: "2.0.0"
description: "Comprehensive adaptive learning toolkit with knowledge gap detection, personalized pathways, difficulty adjustment, spaced repetition, and learning style adaptation for personalized education"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ed-tech", "adaptive-learning", "personalization", "spaced-repetition", "knowledge-gaps"]
category: "ed-tech"
personality: "adaptive-learning-engineer"
use_cases: ["knowledge gap detection", "personalized pathways", "difficulty adjustment", "spaced repetition", "learning style adaptation"]
---

# Adaptive Learning

> Production-grade adaptive learning framework providing knowledge gap detection, personalized learning pathways, difficulty adjustment, spaced repetition scheduling, and learning style adaptation for truly personalized education.

## Overview

The Adaptive Learning module provides tools for creating personalized learning experiences. It implements knowledge gap detection through diagnostic assessment, personalized learning pathway generation, dynamic difficulty adjustment based on performance, spaced repetition scheduling for long-term retention, and learning style adaptation. Every recommendation is based on cognitive science principles and learner data.

## Core Capabilities

### 1. Knowledge Gap Detection
- Diagnostic assessment analysis
- Prerequisite knowledge mapping
- Gap severity classification
- Remediation content recommendation
- Progress tracking through gaps

### 2. Personalized Pathways
- Learning objective sequencing
- Branching content paths
- Adaptive content selection
- Pace adjustment
- Goal-based routing

### 3. Difficulty Adjustment
- Real-time difficulty scaling
- Item Response Theory (IRT) integration
- Zone of Proximal Development targeting
- Challenge level optimization
- Frustration/flow balance

### 4. Spaced Repetition
- SM-2 algorithm implementation
- Review scheduling optimization
- Forgetting curve modeling
- Long-term retention tracking
- Review interval calculation

### 5. Learning Style Adaptation
- Visual/auditory/kinesthetic detection
- Content format optimization
- Presentation style adjustment
- Interaction preference learning
- Multimodal content delivery

### 6. Learning Analytics
- Mastery level tracking
- Learning velocity measurement
- Engagement pattern analysis
- Predictive performance modeling
- Intervention recommendation

## Usage Examples

### Knowledge Gap Detection

```python
from adaptive_learning import GapDetector, DiagnosticAssessment

detector = GapDetector()

# Analyze diagnostic results
gaps = detector.analyze(
    assessment_results={"algebra": 60, "geometry": 85, "calculus": 40},
    target_competencies=["algebra", "geometry", "calculus", "statistics"],
)

print(f"Knowledge gaps: {len(gaps)}")
for gap in gaps:
    print(f"  {gap.topic}: {gap.severity} gap ({gap.current_level:.0f}% → {gap.target_level:.0f}%)")
    print(f"    Remediation: {gap.remediation_content}")
```

### Personalized Pathways

```python
from adaptive_learning import PathwayGenerator, LearnerProfile

generator = PathwayGenerator()

# Generate personalized pathway
pathway = generator.generate(
    learner=LearnerProfile(
        email="student@example.com",
        current_mastery={"algebra": 0.7, "geometry": 0.9},
        learning_style="visual",
        pace="moderate",
    ),
   目标=["master_calculus"],
)

print(f"Pathway: {len(pathway.steps)} steps")
for step in pathway.steps[:5]:
    print(f"  {step.order}: {step.content_title} ({step.estimated_minutes} min)")
```

### Difficulty Adjustment

```python
from adaptive_learning import DifficultyManager

manager = DifficultyManager()

# Adjust difficulty based on performance
new_difficulty = manager.adjust(
    current_difficulty=0.5,
    recent_performance={"correct": 7, "total": 10},
    response_times=[2.1, 3.5, 1.8, 4.2, 2.5],
)

print(f"Difficulty: {manager.current_difficulty:.2f} → {new_difficulty:.2f}")
print(f"Zone: {manager.learning_zone}")  # frustration, flow, boredom
```

### Spaced Repetition

```python
from adaptive_learning import SpacedRepetitionScheduler

scheduler = SpacedRepetitionScheduler()

# Schedule reviews
schedule = scheduler.schedule(
    items=[
        {"id": "concept-1", "mastery": 0.6, "last_review": "2024-01-10"},
        {"id": "concept-2", "mastery": 0.8, "last_review": "2024-01-05"},
        {"id": "concept-3", "mastery": 0.4, "last_review": "2024-01-12"},
    ],
    review_window_days=7,
)

print(f"Reviews scheduled: {len(schedule.reviews)}")
for review in schedule.reviews[:5]:
    print(f"  {review.item_id}: {review.scheduled_date} (priority: {review.priority})")
```

## Best Practices

### Knowledge Gaps
- Use diagnostic assessments before starting a course
- Address foundational gaps before advanced topics
- Provide multiple remediation resources per gap
- Track progress through gap closure

### Personalized Pathways
- Balance learner choice with structured guidance
- Allow pathway revision based on progress
- Provide clear milestones and checkpoints
- Offer both linear and branching options

### Difficulty Adjustment
- Target the Zone of Proximal Development
- Balance challenge with achievability
- Use multiple signals (accuracy, speed, confidence)
- Avoid frustration through gradual adjustment

### Spaced Repetition
- Schedule reviews before forgetting occurs
- Increase intervals as mastery improves
- Combine with active recall techniques
- Respect learner time constraints

## Related Modules

- **learning-platforms**: Platform integration for adaptive features
- **assessment-systems**: Diagnostic and formative assessment
- **student-analytics**: Learning analytics and insights
- **content-delivery**: Adaptive content delivery

---

## Advanced Configuration

### Algorithm Parameters

```python
from adaptive_learning import AdaptiveConfig

config = AdaptiveConfig(
    # IRT Parameters
    irt_parameters={
        "discrimination_range": (0.5, 2.5),
        "difficulty_range": (-3.0, 3.0),
        "guessing_parameter": 0.2,
        "sample_size_threshold": 100,
    },
    
    # Spaced Repetition
    spaced_repetition={
        "initial_interval_days": 1,
        "interval_multiplier": 2.5,
        "max_interval_days": 365,
        "easiness_factor_min": 1.3,
        "easiness_factor_initial": 2.5,
    },
    
    # Difficulty Adjustment
    difficulty_adjustment={
        "target_success_rate": 0.75,
        "adjustment_rate": 0.1,
        "min_responses_for_adjustment": 5,
        "flow_zone_bounds": (0.6, 0.9),
    },
)
```

### Knowledge Graph Configuration

```python
from adaptive_learning import KnowledgeGraphConfig

kg_config = KnowledgeGraphConfig(
    # Graph Structure
    max_depth=10,
    min_mastery_threshold=0.7,
    prerequisite_weight=0.3,
    
    # Edge Types
    edge_types={
        "prerequisite": {"weight": 1.0, "required": True},
        "enables": {"weight": 0.8, "required": False},
        "related": {"weight": 0.5, "required": False},
    },
    
    # Traversal
    traversal_algorithm="dijkstra",
    fallback_to_breadth_first=True,
)
```

## Architecture Patterns

### State Machine for Learning Progression

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│  NEW    │────▶│  DIAGNOSING │────▶│  GAP_FOUND  │
└─────────┘     └─────────────┘     └──────┬──────┘
                                           │
                                           ▼
┌─────────────────┐     ┌─────────────────────────┐
│  REMEDIATING    │◀────│  PATH_GENERATED         │
└────────┬────────┘     └─────────────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│  LEARNING       │────▶│  MASTERY    │
└────────┬────────┘     └─────────────┘
         │
         ▼
┌─────────────────┐
│  REVIEW_SCHEDULED│
└─────────────────┘
```

### Event-Driven Adaptive Engine

```python
from adaptive_learning import EventProcessor, LearningEvent

processor = EventProcessor()

# Process learning events
@processor.on("assessment.completed")
def handle_assessment(event: LearningEvent):
    # Update mastery estimates
    processor.mastery_engine.update(
        learner_id=event.learner_id,
        item_id=event.item_id,
        correct=event.result["correct"],
        response_time=event.result["response_time"],
    )
    
    # Check for knowledge gaps
    gaps = processor.gap_detector.analyze(event.learner_id)
    if gaps:
        processor.emit("gap.detected", {"gaps": gaps})
    
    # Adjust difficulty
    processor.difficulty_engine.adjust(event.learner_id)

@processor.on("gap.detected")
def handle_gap(event: LearningEvent):
    # Generate remediation content
    remediation = processor.remediation_generator.generate(event.data["gaps"])
    processor.emit("content.recommended", {"content": remediation})
```

## Integration Guide

### Learning Platform Integration

```python
from adaptive_learning import LearningPlatformAdapter

adapter = LearningPlatformAdapter()

# Sync learner data
adapter.sync_learner(
    learner_id="learner@example.com",
    platform_data={
        "enrolled_courses": ["course-1", "course-2"],
        "completed_activities": ["act-1", "act-2", "act-3"],
        "assessment_scores": {"q1": 0.8, "q2": 0.6, "q3": 0.9},
    },
)

# Get adaptive recommendations
recommendations = adapter.get_recommendations("learner@example.com")
for rec in recommendations:
    print(f"Recommended: {rec.content_title} (priority: {rec.priority})")
```

### LRS Integration

```python
from adaptive_learning import LRSIntegration

lrs = LRSIntegration(endpoint="https://lrs.example.com")

# Send adaptive learning statements
lrs.send_statement({
    "actor": {"mbox": "mailto:learner@example.com"},
    "verb": {"id": "http://adlnet.gov/expapi/verbs/mastered"},
    "object": {
        "id": "http://example.com/competency/algebra",
        "definition": {"name": {"en": "Algebra"}},
    },
    "result": {
        "score": {"scaled": 0.85},
        "extensions": {
            "http://example.com/ext/mastery_level": 0.85,
            "http://example.com/ext/adaptive_path": "recommended",
        },
    },
})
```

## Performance Optimization

### Model Caching

```python
from adaptive_learning import ModelCache

cache = ModelCache()

# Cache IRT parameters
@cache.cached(ttl=3600)
def get_learner_irt_params(learner_id, item_pool_id):
    return compute_irt_parameters(learner_id, item_pool_id)

# Cache knowledge graph
@cache.cached(ttl=1800)
def get_knowledge_graph(course_id):
    return build_knowledge_graph(course_id)

# Batch processing
batch_results = cache.batch_process(
    learner_ids=["learner1@example.com", "learner2@example.com"],
    compute_fn=get_learner_irt_params,
    batch_size=100,
)
```

### Query Optimization

```python
from adaptive_learning import QueryOptimizer

optimizer = QueryOptimizer()

# Optimize knowledge gap queries
optimizer.add_index("learner_mastery", ["learner_id", "competency_id"])
optimizer.add_index("assessment_results", ["learner_id", "item_id", "timestamp"])

# Materialized view for analytics
optimizer.create_materialized_view(
    "learner_progress_summary",
    """
    SELECT 
        learner_id,
        COUNT(DISTINCT competency_id) as mastered_count,
        AVG(mastery_level) as avg_mastery,
        MAX(updated_at) as last_activity
    FROM learner_mastery
    GROUP BY learner_id
    """,
    refresh_interval="5 minutes",
)
```

## Security Considerations

### Data Privacy

```python
from adaptive_learning import PrivacyManager

privacy = PrivacyManager()

# Anonymize learner data
anonymized = privacy.anonymize(
    data=learner_data,
    fields=["email", "name", "ip_address"],
    method="k_anonymity",
    k=5,
)

# Differential privacy
private_stats = privacy.differential_privacy(
    query="SELECT AVG(mastery_level) FROM learner_mastery",
    epsilon=0.5,
    delta=1e-5,
)
```

### Access Control

```python
from adaptive_learning import AccessControl

ac = AccessControl()

# Restrict access to learner profiles
ac.define_policy(
    name="learner_profile_access",
    rules=[
        {"role": "learner", "access": "own_profile"},
        {"role": "instructor", "access": "course_learners"},
        {"role": "admin", "access": "all_profiles"},
    ],
)

# Check access
can_view = ac.check_access(
    user="instructor@example.com",
    resource="learner_profile",
    resource_id="learner@example.com",
    context={"course_id": "course-123"},
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow recommendations | Large knowledge graph | Cache hot paths, prune low-value edges |
| Inaccurate mastery | Insufficient data | Lower confidence threshold, request more assessments |
| Repetitive content | Poor item selection | Update item pool, adjust selection criteria |
| High latency | Synchronous processing | Move to async, batch recommendations |
| Cold start | New learner | Use demographic priors, onboarding assessment |

### Debug Mode

```python
from adaptive_learning import enable_debug

enable_debug(
    components=["mastery", "gap_detection", "recommendation"],
    log_level="DEBUG",
    trace_decisions=True,
)

# Debug specific learner
debug_session = debug.track_learner("learner@example.com")
print(f"Debug session: {debug_session.id}")
print(f"Trace URL: {debug_session.trace_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/learners/{id}/mastery         Get mastery levels
POST   /api/v1/learners/{id}/mastery         Update mastery
GET    /api/v1/learners/{id}/gaps             Get knowledge gaps
POST   /api/v1/learners/{id}/recommendations  Get recommendations
GET    /api/v1/learners/{id}/schedule         Get review schedule
POST   /api/v1/learners/{id}/schedule         Update schedule
GET    /api/v1/courses/{id}/knowledge-graph   Get knowledge graph
POST   /api/v1/diagnostics/{id}/analyze       Analyze diagnostic
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class MasteryLevel:
    learner_id: UUID
    competency_id: UUID
    level: float  # 0.0 to 1.0
    confidence: float
    last_assessed: datetime
    assessment_count: int

@dataclass
class KnowledgeGap:
    learner_id: UUID
    competency_id: UUID
    current_level: float
    target_level: float
    severity: str  # low, medium, high
    remediation_content: List[str]

@dataclass
class AdaptiveRecommendation:
    learner_id: UUID
    content_id: UUID
    content_type: str
    priority: int
    reason: str
    estimated_duration_minutes: int

@dataclass
class ReviewSchedule:
    learner_id: UUID
    items: List["ReviewItem"]
    next_review: datetime
    total_items: int

@dataclass
class ReviewItem:
    item_id: UUID
    mastery_level: float
    last_reviewed: datetime
    next_review: datetime
    easiness_factor: float
```

## Deployment Guide

### Model Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adaptive-engine
spec:
  replicas: 2
  selector:
    matchLabels:
      app: adaptive-engine
  template:
    spec:
      containers:
      - name: engine
        image: adaptive-engine:latest
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: MODEL_CACHE_SIZE
          value: "1000"
        - name: BATCH_SIZE
          value: "100"
```

## Monitoring & Observability

### Key Metrics

```python
from adaptive_learning import Metrics

metrics = Metrics()

# Track recommendation accuracy
metrics.track(
    "recommendation.accuracy",
    accuracy_score,
    tags={"content_type": "video", "difficulty": "medium"},
)

# Track mastery changes
metrics.histogram(
    "mastery.level_change",
    level_change,
    tags={"competency": "algebra"},
)

# Track latency
metrics.timer(
    "recommendation.latency_ms",
    latency,
    tags={"endpoint": "get_recommendations"},
)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from adaptive_learning import MasteryEngine, GapDetector

@pytest.fixture
def mastery_engine():
    return MasteryEngine(test_mode=True)

def test_mastery_update(mastery_engine):
    mastery_engine.update(
        learner_id="learner-1",
        competency_id="algebra",
        correct=True,
        response_time=2.5,
    )
    mastery = mastery_engine.get_level("learner-1", "algebra")
    assert mastery.level > 0.0

def test_gap_detection():
    detector = GapDetector()
    gaps = detector.analyze(
        mastery_levels={"algebra": 0.3, "geometry": 0.9},
        target_levels={"algebra": 0.7, "geometry": 0.7},
    )
    assert len(gaps) == 1
    assert gaps[0].competency == "algebra"
```

## Versioning & Migration

### Version History

- **2.0.0**: Added knowledge graph, IRT integration, improved gap detection
- **1.5.0**: Added spaced repetition, difficulty adjustment
- **1.0.0**: Initial release with basic adaptive recommendations

### Migration Guide

```python
from adaptive_learning import Migration

# Migrate from v1 to v2
migration = Migration(from_version="1.x", to_version="2.0.0")
migration.execute(
    data_path="/data/adaptive_v1",
    output_path="/data/adaptive_v2",
    validate=True,
)
```

## Glossary

| Term | Definition |
|------|------------|
| **IRT** | Item Response Theory - statistical model for assessment items |
| **Mastery** | Demonstrated competency level (0.0-1.0) |
| **Knowledge Gap** | Difference between current and target mastery |
| **Zone of Proximal Development** | Optimal challenge range for learning |
| **Spaced Repetition** | Reviewing material at increasing intervals |
| **Easiness Factor** | Difficulty multiplier in spaced repetition |
| **SM-2** | SuperMemo 2 algorithm for spaced repetition |

## Changelog

### Version 2.0.0
- Knowledge graph integration
- IRT-based difficulty estimation
- Improved gap detection algorithms
- Batch recommendation processing

### Version 1.5.0
- Spaced repetition scheduling
- Dynamic difficulty adjustment
- Learning style detection

### Version 1.0.0
- Initial release
- Basic adaptive recommendations
- Simple mastery tracking

## Contributing Guidelines

1. Follow coding standards
2. Write unit tests for algorithms
3. Document parameter changes
4. Validate with real learner data
5. Submit pull request

## Adaptive Learning Analytics

### Learner Progress Dashboard

```python
from adaptive_learning import ProgressDashboard

dashboard = ProgressDashboard()

# Generate progress report
report = dashboard.generate(
    learner_id="learner@example.com",
    course_id="python-101",
    time_range_days=30,
)

print(f"Learner Progress:")
print(f"  Mastery Level: {report.mastery_level:.0%}")
print(f"  Learning Velocity: {report.velocity:.2f} concepts/day")
print(f"  Time on Task: {report.total_hours:.1f} hours")
print(f"  Completion: {report.completion_rate:.0%}")
print(f"  Streak: {report.current_streak_days} days")
```

### Learning Outcome Prediction

```python
from adaptive_learning import OutcomePredictor

predictor = OutcomePredictor()

# Predict learning outcomes
prediction = predictor.predict(
    learner_id="learner@example.com",
    course_id="python-101",
    current_progress={
        "modules_completed": 5,
        "total_modules": 12,
        "avg_score": 0.82,
        "time_spent_hours": 8.5,
    },
)

print(f"Outcome Prediction:")
print(f"  Predicted Grade: {prediction.predicted_grade}")
print(f"  Completion Probability: {prediction.completion_probability:.0%}")
print(f"  Time to Complete: {prediction.estimated_hours_remaining:.1f} hours")
print(f"  Risk Factors: {prediction.risk_factors}")
```

## Adaptive Learning System Architecture

### Multi-Armed Bandit for Content Selection

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class BanditArm:
    content_id: str
    subject: str
    difficulty: float
    reward_sum: float = 0.0
    pull_count: int = 0
    last_pulled: float = 0.0
    
    @property
    def estimated_reward(self) -> float:
        if self.pull_count == 0:
            return float('inf')
        return self.reward_sum / self.pull_count
    
    def update(self, reward: float):
        self.reward_sum += reward
        self.pull_count += 1
        self.last_pulled = time.time()

class ThompsonSamplingSelector:
    def __init__(self, alpha_prior: float = 1.0, beta_prior: float = 1.0):
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
        self.arms: List[BanditArm] = []
    
    def add_arm(self, arm: BanditArm):
        self.arms.append(arm)
    
    def select(self, context: Dict) -> BanditArm:
        samples = []
        for arm in self.arms:
            alpha = self.alpha_prior + arm.reward_sum
            beta = self.beta_prior + (arm.pull_count - arm.reward_sum)
            sample = np.random.beta(alpha, beta)
            difficulty_match = 1.0 - abs(arm.difficulty - context.get("mastery", 0.5))
            weighted = sample * (0.7 + 0.3 * difficulty_match)
            samples.append((weighted, arm))
        samples.sort(key=lambda x: x[0], reverse=True)
        return samples[0][1]

class AdaptiveLearningEngine:
    def __init__(self):
        self.bandit = ThompsonSamplingSelector()
        self.learner_profiles: Dict[str, Dict] = {}
        self.knowledge_state: Dict[str, Dict[str, float]] = {}
    
    def update_knowledge_state(self, learner_id: str, skill_id: str, correct: bool, 
                                response_time_ms: float, hint_used: bool):
        state = self.knowledge_state.setdefault(learner_id, {}).setdefault(skill_id, {
            "mastery": 0.0, "attempts": 0, "streak": 0,
            "avg_response_time": 0.0, "hint_rate": 0.0,
        })
        state["attempts"] += 1
        if correct:
            state["streak"] += 1
            state["mastery"] = min(1.0, state["mastery"] + 0.1 * (1.0 + 0.1 * state["streak"]))
        else:
            state["streak"] = 0
            state["mastery"] = max(0.0, state["mastery"] - 0.05)
        n = state["attempts"]
        state["avg_response_time"] += (response_time_ms - state["avg_response_time"]) / n
        state["hint_rate"] += ((1.0 if hint_used else 0.0) - state["hint_rate"]) / n
    
    def recommend_next(self, learner_id: str, available_content: List[BanditArm]) -> BanditArm:
        mastery = self._get_average_mastery(learner_id)
        context = {"mastery": mastery, "learner_id": learner_id}
        for arm in available_content:
            if arm.content_id not in [a.content_id for a in self.bandit.arms]:
                self.bandit.add_arm(arm)
        return self.bandit.select(context)
    
    def _get_average_mastery(self, learner_id: str) -> float:
        states = self.knowledge_state.get(learner_id, {})
        if not states:
            return 0.0
        return sum(s["mastery"] for s in states.values()) / len(states)

class SpacedRepetitionScheduler:
    INTERVALS = [1, 3, 7, 14, 30, 60, 120]
    
    def __init__(self):
        self.cards: Dict[str, Dict] = {}
    
    def schedule(self, card_id: str, quality: int):
        card = self.cards.setdefault(card_id, {"interval_idx": 0, "ease_factor": 2.5, "reviews": 0})
        card["reviews"] += 1
        if quality >= 3:
            card["interval_idx"] = min(card["interval_idx"] + 1, len(self.INTERVALS) - 1)
        else:
            card["interval_idx"] = max(0, card["interval_idx"] - 1)
        card["ease_factor"] = max(1.3, card["ease_factor"] + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        interval = self.INTERVALS[card["interval_idx"]] * card["ease_factor"]
        card["next_review"] = time.time() + interval * 86400
        return card["next_review"]
    
    def get_due_cards(self) -> List[str]:
        now = time.time()
        return [cid for cid, c in self.cards.items() if c.get("next_review", 0) <= now]
```

### Learning Path Optimization

```python
from enum import Enum
import heapq

class PrerequisiteType(Enum):
    HARD = "hard"
    SOFT = "soft"
    COREQUISITE = "coreq"

@dataclass
class LearningNode:
    node_id: str
    title: str
    skill_ids: List[str]
    estimated_hours: float
    difficulty: float
    prerequisites: List[tuple]
    learning_objects: List[str]

class LearningPathOptimizer:
    def __init__(self, graph: Dict[str, LearningNode]):
        self.graph = graph
    
    def find_shortest_path(self, start_id: str, target_skill: str) -> List[str]:
        distances = {nid: float('inf') for nid in self.graph}
        distances[start_id] = 0
        predecessors = {nid: None for nid in self.graph}
        pq = [(0, start_id)]
        completed = set()
        
        while pq:
            dist, node_id = heapq.heappop(pq)
            if node_id in completed:
                continue
            completed.add(node_id)
            node = self.graph[node_id]
            for neighbor_id, _ in node.prerequisites:
                if neighbor_id not in self.graph:
                    continue
                new_dist = dist + self.graph[neighbor_id].estimated_hours
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    predecessors[neighbor_id] = node_id
                    heapq.heappush(pq, (new_dist, neighbor_id))
        
        best_target = None
        best_dist = float('inf')
        for nid, node in self.graph.items():
            if target_skill in node.skill_ids and distances[nid] < best_dist:
                best_dist = distances[nid]
                best_target = nid
        
        if best_target is None:
            return []
        
        path = []
        current = best_target
        while current is not None:
            path.append(current)
            current = predecessors[current]
        return list(reversed(path))
```

### Real-Time Difficulty Calibration

```python
class DifficultyCalibrator:
    def __init__(self, target_success_rate: float = 0.75):
        self.target = target_success_rate
        self.window_size = 20
        self.history: Dict[str, List[float]] = {}
    
    def record_outcome(self, content_id: str, correct: bool):
        self.history.setdefault(content_id, []).append(1.0 if correct else 0.0)
    
    def calibrate_difficulty(self, content_id: str) -> float:
        outcomes = self.history.get(content_id, [])
        if len(outcomes) < 5:
            return 0.5
        recent = outcomes[-self.window_size:]
        success_rate = sum(recent) / len(recent)
        if success_rate > self.target + 0.1:
            return min(1.0, 0.5 + (success_rate - self.target) * 0.5)
        elif success_rate < self.target - 0.1:
            return max(0.0, 0.5 - (self.target - success_rate) * 0.5)
        return 0.5
    
    def get_irt_params(self, content_id: str) -> Dict:
        outcomes = self.history.get(content_id, [])
        if len(outcomes) < 10:
            return {"discrimination": 1.0, "difficulty": 0.5, "guessing": 0.2}
        p = sum(outcomes) / len(outcomes)
        discrimination = min(2.0, max(0.5, abs(p - 0.5) * 4.0))
        guessing = max(0.0, min(0.35, 0.25 if p > 0.9 else 0.0))
        return {"discrimination": discrimination, "difficulty": p, "guessing": guessing}

class CognitiveLoadMonitor:
    def __init__(self):
        self.max_cognitive_load = 0.8
        self.history: Dict[str, List[float]] = {}
    
    def estimate_load(self, learner_id: str, task_params: Dict) -> float:
        base = task_params.get("difficulty", 0.5)
        novelty = task_params.get("novelty", 0.5)
        complexity = task_params.get("complexity", 0.5)
        fatigue = self._get_fatigue(learner_id)
        return min(1.0, 0.4 * base + 0.3 * novelty + 0.2 * complexity + 0.1 * fatigue)
    
    def _get_fatigue(self, learner_id: str) -> float:
        history = self.history.get(learner_id, [])
        if len(history) < 3:
            return 0.0
        recent = history[-10:]
        trend = (recent[-1] - recent[0]) / len(recent) if len(recent) > 1 else 0
        return min(1.0, max(0.0, recent[-1] + trend * 0.5))
    
    def should_suggest_break(self, learner_id: str) -> bool:
        return self._get_fatigue(learner_id) > self.max_cognitive_load

class EngagementTracker:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
    
    def start_session(self, learner_id: str) -> str:
        import uuid
        session_id = str(uuid.uuid4())[:8]
        self.sessions.setdefault(learner_id, []).append({
            "session_id": session_id, "start": time.time(),
            "interactions": 0, "content_viewed": 0,
        })
        return session_id
    
    def record_interaction(self, learner_id: str, interaction_type: str):
        sessions = self.sessions.get(learner_id, [])
        if sessions:
            sessions[-1]["interactions"] += 1
            if interaction_type == "content_view":
                sessions[-1]["content_viewed"] += 1
    
    def end_session(self, learner_id: str):
        sessions = self.sessions.get(learner_id, [])
        if sessions and "end" not in sessions[-1]:
            sessions[-1]["end"] = time.time()
            sessions[-1]["duration_seconds"] = sessions[-1]["end"] - sessions[-1]["start"]
    
    def calculate_engagement_score(self, learner_id: str) -> float:
        sessions = self.sessions.get(learner_id, [])
        if not sessions:
            return 0.0
        recent = sessions[-10:]
        total_duration = sum(s.get("duration_seconds", 0) for s in recent)
        total_interactions = sum(s.get("interactions", 0) for s in recent)
        avg_duration = total_duration / len(recent) / 3600
        avg_interactions = total_interactions / len(recent)
        consistency = len(set(
            time.strftime("%Y-%m-%d", time.localtime(s["start"])) for s in recent
        )) / max(1, len(recent))
        return min(100, (avg_duration * 20) + (avg_interactions * 2) + (consistency * 30))
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
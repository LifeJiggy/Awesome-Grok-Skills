# Full-Stack Planner Agent — System Architecture

## 1. Executive Summary

The Full-Stack Planner Agent is a comprehensive project management and technical planning platform for software development teams. It provides tools for tech stack evaluation, sprint planning, resource allocation, risk management, cost estimation, architecture design, technical debt tracking, and performance benchmarking.

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      FULL-STACK PLANNER AGENT                             │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Tech Stack  │  │    Sprint    │  │   Resource   │  │   Risk     │  │
│  │  Evaluator   │  │   Planner    │  │  Allocator   │  │  Manager   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │    Cost      │  │ Architecture │  │  Tech Debt   │  │   Perf     │  │
│  │  Estimator   │  │   Designer   │  │  Tracker     │  │ Benchmarks │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Project Roadmap & Timeline                     │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              Data Models (Task, Sprint, TeamMember, Risk, ADR)   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep Dives

### 3.1 Tech Stack Evaluator

Multi-criteria decision analysis engine for technology selection.

**Evaluation Dimensions:**
- Community Score (0-10): GitHub stars, Stack Overflow activity, contributor count
- Performance Score (0-10): Benchmarks, production usage at scale
- Learning Curve (0-10): Documentation quality, onboarding time
- Ecosystem Score (0-10): Libraries, tools, integrations
- Cost (monthly): Licensing, infrastructure, support

**Composite Score Formula:**
```
score = 0.20 × community + 0.25 × performance + 0.15 × learning
      + 0.25 × ecosystem + 0.15 × (10 - cost/100)
```

**Workflow:**
```
  Requirements Analysis
         │
         ▼
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Register     │ ──► │ Evaluate by  │ ──► │ Recommend    │
  │ Candidates   │     │ Category     │     │ Best Stack   │
  └──────────────┘     └──────────────┘     └──────────────┘
         │                                          │
         └──────────────────────────────────────────┘
                        Compare Options
```

### 3.2 Sprint Planner

Scrum sprint lifecycle management with velocity tracking and burndown analysis.

**Key Features:**
- Sprint creation with configurable duration (default 14 days)
- Task assignment with story point tracking
- Velocity calculation (rolling average)
- Burndown chart data generation
- Sprint completion with carry-over analysis
- Predictive completion estimation

**Velocity Model:**
```
Average Velocity = Σ(completed_points) / num_sprints
Predicted Sprints = remaining_points / avg_velocity
```

**Sprint Lifecycle:**
```
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Planning │ ─► │  Active  │ ─► │  Review  │ ─► │ Retro-   │
  │          │    │          │    │          │    │ spective │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
  Add tasks      Update status   Complete sprint   Learn & improve
  Set goal       Daily standup   Demo work         Adjust process
```

### 3.3 Resource Allocator

Team capacity management and workload optimization.

**Capacity Model:**
```
Effective Hours = Available Hours × Productivity Factor
Remaining = Effective Hours × (1 - Current Load %)
```

**Workload Rebalancing Algorithm:**
1. Identify overloaded members (load > 90%)
2. Identify underloaded members (load < 50%)
3. Calculate transferable hours (20% of overload)
4. Match by skill compatibility
5. Suggest transfers

**Best-Fit Matching:**
```
  Find candidates with:
    1. Sufficient remaining capacity
    2. Required skills (maximize overlap)
    3. Rank by (skill_match, remaining_capacity)
```

### 3.4 Risk Manager

Quantitative risk assessment with probability × impact scoring.

**Risk Classification:**

| Score Range | Level | Action |
|-------------|-------|--------|
| 7.0 - 10.0 | CRITICAL | Immediate mitigation or avoidance |
| 5.0 - 6.9 | HIGH | Active mitigation required |
| 3.0 - 4.9 | MEDIUM | Monitor and plan mitigation |
| 1.0 - 2.9 | LOW | Accept with monitoring |
| 0.0 - 0.9 | NEGLIGIBLE | Accept |

**Mitigation Strategies:**
- Reduce probability: Controls, testing, process gates
- Reduce impact: Fallbacks, redundancy, insurance
- Transfer: Contracts, insurance, outsourcing
- Avoid: Eliminate the risky activity
- Accept: Monitor and budget for contingency

### 3.5 Cost Estimator

Multi-component cost modeling with contingency.

**Cost Categories:**
- Labor: hours × rate × (1 + contingency%)
- Infrastructure: monthly hosting costs × 12
- Third-party: monthly SaaS/API costs × 12
- Contingency: typically 15-25% of labor

**Budget Report:**
```
  Total Labor = Σ(hours × rate × (1 + contingency))
  Total Infrastructure = Σ(monthly_infra × 12)
  Total Third-Party = Σ(monthly_saas × 12)
  Grand Total = Labor + Infrastructure + Third-Party
```

### 3.6 Architecture Designer

Architecture Decision Record (ADR) management and component documentation.

**ADR Structure:**
```
  ADR-001: Title
  ├── Context: Why this decision was needed
  ├── Decision: What was decided
  ├── Consequences: Positive and negative outcomes
  └── Alternatives: Other options considered
```

**Supported Architecture Styles:**
- Monolith: Single deployment unit
- Microservices: Independently deployable services
- Serverless: Function-as-a-Service
- Event-Driven: Message-based communication
- Modular Monolith: Well-separated modules in single deployment
- CQRS: Command-Query Responsibility Segregation
- Layered: Traditional N-tier
- Hexagonal: Ports and adapters

### 3.7 Tech Debt Tracker

Technical debt management with interest modeling.

**Debt Cost Model:**
```
Total Cost (if unfixed) = Fix Hours + (Interest per Sprint × Sprints)
Priority Score = Interest × 10 + Fix Hours
```

**Categories:**
- Code debt: Code smells, duplication, complexity
- Architecture debt: Tight coupling, wrong patterns
- Test debt: Missing or inadequate tests
- Documentation debt: Missing or outdated docs
- Infrastructure debt: Outdated dependencies, manual processes

### 3.8 Performance Benchmarks

SLA and performance target tracking.

**Threshold Levels:**
- Target: Desired performance level
- Warning: Acceptable degradation threshold
- Critical: Unacceptable performance level

---

## 4. Data Flow

```
  ┌──────────────────────────────────────────────────────────────┐
  │                     PROJECT INITIATION                        │
  │  Requirements ──► Tech Evaluation ──► Architecture Design     │
  └──────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     PLANNING PHASE                            │
  │  Cost Estimation ──► Risk Assessment ──► Roadmap Creation     │
  └──────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     EXECUTION PHASE                           │
  │  Sprint Planning ──► Resource Allocation ──► Task Execution   │
  │       │                    │                     │            │
  │       ▼                    ▼                     ▼            │
  │  Velocity Tracking   Load Balancing      Status Updates       │
  └──────────────────────────────┬───────────────────────────────┘
                                 │
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     MONITORING & CONTROL                      │
  │  Burndown Charts ──► Risk Review ──► Debt Tracking            │
  │       │                    │                │                 │
  │       ▼                    ▼                ▼                 │
  │  Progress Reports    Mitigation       Prioritized Backlog    │
  └──────────────────────────────────────────────────────────────┘
```

---

## 5. Design Patterns

### Strategy Pattern
Different estimation strategies, risk models, and allocation algorithms can be swapped via protocols.

### Observer Pattern (via Event Model)
Sprint events (planning, review, retrospective) trigger workflow transitions.

### Record Pattern (ADR)
Architecture decisions are immutable records with clear lifecycle (proposed → accepted → deprecated).

### Composite Pattern
Epics contain tasks, sprints contain tasks, projects contain sprints — hierarchical composition.

---

## 6. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | Type hints + dataclasses |
| Enums | Enum, IntEnum |
| Collections | defaultdict, list |
| Date/Time | datetime, timedelta |
| Math | math (for calculations) |
| Logging | Python logging |
| Dependencies | Zero (stdlib only) |

---

## 7. Security Considerations

### Data Protection
- No external network calls — all data processed in-memory
- No persistent storage by default
- Sensitive data (team rates, budgets) kept in memory only

### Access Control
- No authentication layer (embedded component)
- Caller controls data access
- Audit trail via logging

### Input Validation
- Bounds checking on probabilities (0-1), impacts (0-10)
- Positive value validation for hours, costs, story points
- Date range validation for sprints

---

## 8. Scalability

### Current Limits
- ~1,000 tasks per project (memory)
- ~100 team members (allocation matrix)
- ~50 sprints (velocity history)

### Scaling Strategies
1. **Database backend**: Replace in-memory dicts with PostgreSQL
2. **API layer**: Add REST/GraphQL endpoints for multi-user access
3. **Caching**: Cache computed metrics (velocity, capacity)
4. **Async**: Process large task sets asynchronously
5. **Multi-project**: Add project isolation layer

---

## 9. Extension Points

### Custom Estimation Strategy
```python
class StoryPointEstimator:
    def estimate(self, tasks: List[Task]) -> float:
        # Custom estimation logic
        return sum(t.story_points for t in tasks)
```

### Custom Risk Model
Extend `RiskManager._classify_risk()` with domain-specific thresholds.

### Custom Architecture Style
Add new `ArchitectureStyle` enum variants and update the designer.

### Integration Points
- Jira/Azure DevOps: Import/export tasks
- Slack/Teams: Notification integration
- GitHub: Link tasks to issues/PRs
- Confluence: Auto-generate documentation

---

## 10. Testing Strategy

### Unit Tests
- TechStackEvaluator: Score calculation, ranking consistency
- SprintPlanner: Velocity computation, burndown accuracy
- ResourceAllocator: Capacity math, rebalancing logic
- RiskManager: Classification thresholds, score computation
- CostEstimator: Budget aggregation, task-to-cost conversion

### Integration Tests
- Sprint lifecycle: Create → Plan → Execute → Complete
- Resource allocation with real task dependencies
- Risk mitigation suggestion accuracy

### Property-Based Tests
- Weights sum to 1.0 in tech evaluation
- Velocity is non-negative
- Capacity utilization ≤ 100%
- Risk scores = probability × impact

---

## 11. Future Enhancements

### Short-term
- Gantt chart generation
- Kanban board view
- Time tracking integration
- Automated sprint retrospective analysis

### Medium-term
- Machine learning for effort estimation
- Natural language task creation
- Auto-generated architecture diagrams
- Risk prediction from historical data

### Long-term
- Multi-team coordination
- Portfolio-level planning across projects
- Real-time collaboration
- AI-powered project insights

---

## 12. Detailed Component Internals

### 12.1 Tech Stack Evaluator Internals

**Score Calculation:**
```
  score = 0.20 × community + 0.25 × performance + 0.15 × learning
        + 0.25 × ecosystem + 0.15 × (10 - cost/100)
```

**Ranking Algorithm:**
1. Filter by required category
2. Calculate composite score for each candidate
3. Sort by score descending
4. Return ranked list with scores

**Comparison Logic:**
```
  compare(tech_a, tech_b):
      score_a = calculate_score(tech_a)
      score_b = calculate_score(tech_b)
      difference = score_a - score_b
      return {
          "winner": tech_a if difference > 0 else tech_b,
          "margin": abs(difference),
          "breakdown": {...}
      }
```

### 12.2 Sprint Planner Internals

**Velocity Calculation:**
```
  velocity = sum(completed_points) / count(completed_sprints)
  predicted_sprints = remaining_points / velocity
```

**Burndown Data:**
```
  for each day in sprint:
      ideal_remaining = total_points × (1 - day / total_days)
      actual_remaining = sum(remaining_points for incomplete tasks)
      burndown.append({day, ideal, actual})
```

**Sprint Completion Logic:**
```
  complete_sprint(sprint_id):
      1. Mark incomplete tasks as carry-over
      2. Calculate velocity (completed_points)
      3. Update velocity history
      4. Generate completion report
      5. Return metrics
```

### 12.3 Resource Allocator Internals

**Capacity Calculation:**
```
  effective_hours = available_hours × productivity_factor
  remaining = effective_hours × (1 - current_load_pct)
```

**Best-Fit Algorithm:**
```
  find_best_fit(required_skills, hours_needed):
      candidates = []
      for member in team:
          skill_match = len(set(required_skills) & set(member.skills))
          if member.remaining_capacity >= hours_needed:
              candidates.append((member, skill_match, member.remaining_capacity))
      
      # Sort by skill match (desc), then remaining capacity (desc)
      candidates.sort(key=lambda x: (-x[1], -x[2]))
      return candidates[0] if candidates else None
```

**Workload Rebalancing:**
```
  rebalance_workload():
      overloaded = [m for m in team if m.load > 0.9]
      underloaded = [m for m in team if m.load < 0.5]
      
      suggestions = []
      for over in overloaded:
          transfer_hours = over.overload_hours × 0.2
          best_match = find_best_match(over.skills, underloaded)
          if best_match:
              suggestions.append({
                  "from": over,
                  "to": best_match,
                  "hours": transfer_hours
              })
      return suggestions
```

### 12.4 Risk Manager Internals

**Risk Score Calculation:**
```
  risk_score = probability × impact
```

**Classification Thresholds:**
```
  if score >= 7.0: CRITICAL
  elif score >= 5.0: HIGH
  elif score >= 3.0: MEDIUM
  elif score >= 1.0: LOW
  else: NEGLIGIBLE
```

**Mitigation Suggestion Logic:**
```
  suggest_mitigations(risk_id):
      risk = get_risk(risk_id)
      suggestions = []
      
      if risk.probability > 0.7:
          suggestions.append("Reduce probability through controls")
      if risk.impact > 7:
          suggestions.append("Reduce impact through redundancy")
      if risk.probability × risk.impact > 5:
          suggestions.append("Consider risk transfer (insurance)")
      
      return suggestions
```

---

## 13. Error Handling Strategy

### 13.1 Input Validation

| Component | Validation | Error Type |
|-----------|------------|------------|
| SprintPlanner | Valid dates, non-empty tasks | ValueError |
| ResourceAllocator | Positive hours, valid skills | ValueError |
| RiskManager | Probability 0-1, impact 0-10 | ValueError |
| CostEstimator | Positive costs, valid rates | ValueError |
| ArchitectureDesigner | Non-empty names, valid style | ValueError |

### 13.2 Graceful Degradation

- **Insufficient data**: Return partial results with warnings
- **Invalid configuration**: Use defaults with notification
- **Missing dependencies**: Skip dependent calculations

---

## 14. Testing Architecture

### 14.1 Test Categories

| Category | Coverage | Tools |
|----------|----------|-------|
| Unit Tests | Individual methods | pytest |
| Integration Tests | Component interaction | pytest |
| Property Tests | Mathematical invariants | hypothesis |
| Edge Cases | Boundary conditions | pytest |

### 14.2 Test Data Strategy

- **Synthetic data**: Generated with known outcomes
- **Edge cases**: Empty teams, zero capacity, extreme risks
- **Real-world scenarios**: Based on typical projects

---

## 15. Configuration Management

### 15.1 Default Configuration

```python
DEFAULT_CONFIG = {
    "sprint_duration_days": 14,
    "working_hours_per_day": 8.0,
    "working_days_per_week": 5,
    "risk_tolerance": "medium",
    "default_hourly_rate": 100.0,
    "contingency_percentage": 0.2,
    "velocity_history_size": 5,
}
```

### 15.2 Risk Tolerance Thresholds

```python
RISK_THRESHOLDS = {
    "low": 3.0,
    "medium": 5.0,
    "high": 7.0,
}
```

---

## 16. Logging and Monitoring

### 16.1 Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed calculation steps |
| INFO | Sprint creation, task completion |
| WARNING | Capacity exceeded, risk threshold |
| ERROR | Invalid inputs, calculation failures |

### 16.2 Metrics to Monitor

- Sprint velocity trends
- Team utilization rates
- Risk score distributions
- Budget variance
- Technical debt growth rate

---

## 17. Future Roadmap

### 17.1 Short-term Enhancements

- Gantt chart generation
- Kanban board view
- Time tracking integration
- Automated sprint retrospective analysis

### 17.2 Medium-term Enhancements

- Machine learning for effort estimation
- Natural language task creation
- Auto-generated architecture diagrams
- Risk prediction from historical data

### 17.3 Long-term Vision

- Multi-team coordination
- Portfolio-level planning across projects
- Real-time collaboration
- AI-powered project insights

---

## 18. Comparison with Industry Tools

| Feature | Full-Stack Planner | Jira | Asana | Linear |
|---------|-------------------|------|-------|--------|
| Dependencies | Zero | Cloud | Cloud | Cloud |
| Tech Stack Eval | Built-in | Via plugins | No | No |
| Sprint Planning | Built-in | Built-in | Built-in | Built-in |
| Resource Mgmt | Built-in | Via plugins | Basic | Basic |
| Risk Mgmt | Built-in | Via plugins | No | No |
| Cost Estimation | Built-in | No | No | No |
| Architecture | Built-in | No | No | No |
| Cost | Free | $8/user/mo | $11/user/mo | $8/user/mo |

---

**See Also**: [GROK.md](./GROK.md) for agent identity and capabilities,
[README.md](./README.md) for quick start and API reference.
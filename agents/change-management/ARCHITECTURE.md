# Change Management Agent — Architecture

## 1. Overview

The Change Management Agent is a comprehensive organizational change orchestration system designed to manage enterprise-scale transformations from initiation through institutionalization. It implements the ADKAR individual change model alongside Kotter's 8-step framework, providing a dual-lens approach to change readiness and resistance management.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     CHANGE MANAGEMENT AGENT v2.0                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                        ORCHESTRATOR LAYER                         │  │
│  │  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────────┐  │  │
│  │  │  Change   │ │ Stakeholder  │ │ ADKAR    │ │ Communication  │  │  │
│  │  │  Plan     │ │ Analysis     │ │ Model    │ │ Planner        │  │  │
│  │  │  Manager  │ │ Engine       │ │ Evaluator│ │                │  │  │
│  │  └────┬─────┘ └──────┬───────┘ └────┬─────┘ └───────┬────────┘  │  │
│  │       │              │              │               │             │  │
│  │  ┌────┴─────┐ ┌──────┴───────┐ ┌────┴─────┐ ┌──────┴────────┐  │  │
│  │  │Resistance│ │  Training    │ │ Readiness│ │ Notification  │  │  │
│  │  │ Manager  │ │  Developer   │ │ Assessor │ │ Engine        │  │  │
│  │  └──────────┘ └──────────────┘ └──────────┘ └───────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌─────────────────────────────────┴──────────────────────────────────┐  │
│  │                         DATA LAYER                                 │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │  │
│  │  │  Change  │ │Stakeholder│ │ Training │ │ Evidence │            │  │
│  │  │  Plans   │ │ Profiles │ │ Modules  │ │ Store    │            │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

## 2. System Components

### 2.1 Orchestrator Layer

The orchestrator layer contains the core intelligence of the system. Each component operates independently but shares state through the central ChangePlan data structure.

#### Change Plan Manager
- Creates and maintains change initiative plans
- Manages plan lifecycle (draft → planning → approved → in_progress → completed)
- Generates phase plans with configurable timelines
- Tracks milestones and deliverables

#### Stakeholder Analyzer
- Maps stakeholders on a power/interest grid
- Classifies by influence, engagement, and resistance levels
- Identifies potential change champions
- Generates tailored engagement strategies per stakeholder
- Tracks stakeholder evolution over time

#### ADKAR Model Evaluator
- Evaluates individual readiness across five dimensions
- Identifies bottlenecks (earliest failing phase)
- Compares readiness across stakeholder cohorts
- Computes organizational aggregate readiness
- Generates phase-specific recommendations

#### Communication Planner
- Creates structured communication plans across channels
- Generates stakeholder-group-specific messaging
- Schedules communications across the change timeline
- Tracks communication effectiveness and feedback

#### Resistance Manager
- Assesses resistance levels per stakeholder
- Creates intervention plans with escalation paths
- Tracks resistance trends over time
- Provides summary dashboards for executive reporting

#### Training Developer
- Auto-generates training modules aligned to ADKAR phases
- Manages enrollment, completion, and scoring
- Tracks training effectiveness metrics
- Supports multiple delivery formats

#### Readiness Assessor
- Evaluates organizational readiness across 8 dimensions
- Identifies gaps and strengths
- Generates dimension-specific recommendations
- Tracks readiness trends over time

### 2.2 Data Layer

All data is stored in-memory during agent execution. The data layer consists of:

| Store | Content | Key Entity |
|-------|---------|------------|
| Change Plans | Initiative definitions, phases, objectives | ChangePlan |
| Stakeholder Profiles | Influence, resistance, concerns, engagement | Stakeholder |
| Training Modules | ADKAR-aligned learning units | TrainingModule |
| Communication Plans | Scheduled messages, channels, audiences | CommunicationMessage |
| Risk Register | Identified risks, scores, mitigations | RiskItem |
| Evidence Store | Audit trail, documentation references | Evidence |

## 3. Data Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  User   │───>│  Create  │───>│  Assess  │───>│  Plan    │
│ Request │    │  Plan    │    │ Readiness│    │ Actions  │
└─────────┘    └──────────┘    └──────────┘    └──────────┘
                                      │               │
                                      v               v
                               ┌──────────┐    ┌──────────┐
                               │  ADKAR   │    │Comms/    │
                               │  Eval    │    │Training  │
                               └──────────┘    └──────────┘
                                      │               │
                                      v               v
                               ┌──────────────────────────┐
                               │     Execute & Monitor     │
                               │  (Resistance + Training)  │
                               └──────────────┬───────────┘
                                              │
                                              v
                               ┌──────────────────────────┐
                               │    Reinforcement &       │
                               │    Institutionalization   │
                               └──────────────────────────┘
```

### 3.1 Detailed Data Flow

1. **Plan Creation**: User initiates a change plan → phases and milestones auto-generated
2. **Stakeholder Onboarding**: Stakeholders added → resistance assessed → engagement strategy generated
3. **ADKAR Evaluation**: Each stakeholder scored → bottlenecks identified → interventions planned
4. **Communication Development**: Channels mapped → messages scheduled → cadence established
5. **Training Program**: Modules created → enrollments tracked → completions recorded
6. **Readiness Assessment**: Organizational dimensions scored → gaps identified → recommendations generated
7. **Resistance Monitoring**: Continuous tracking → trend analysis → escalation triggers
8. **Reinforcement**: Success metrics tracked → regression detected → sustainment activities scheduled

## 4. Design Patterns

### 4.1 Strategy Pattern
Each resistance level maps to a distinct intervention strategy through the `ResistanceManager.INTERVENTION_STRATEGIES` dictionary. This allows strategy selection based on runtime conditions without conditional branching.

### 4.2 Observer Pattern
The `ResistanceManager` and `StakeholderAnalyzer` maintain history logs that record state changes over time, enabling trend analysis and retrospective comparison.

### 4.3 Builder Pattern
The `ChangePlan` dataclass is constructed incrementally — stakeholders, communications, training modules, and risks are added in separate steps, allowing flexible plan composition.

### 4.4 Chain of Responsibility
ADKAR evaluation follows a chain: Awareness → Desire → Knowledge → Ability → Reinforcement. Each phase must pass before the next is meaningful, and the bottleneck is always the first failing phase.

### 4.5 Composite Pattern
Training programs are composed of individual modules, each targeting a specific ADKAR phase. The `TrainingDeveloper` aggregates these into a coherent program.

## 5. Component Deep Dive

### 5.1 ADKAR Model Evaluator

```
┌────────────────────────────────────────────────┐
│              ADKAR Evaluation Flow              │
├────────────────────────────────────────────────┤
│                                                │
│  Input: {awareness: 0.8, desire: 0.6, ...}    │
│            │                                   │
│            v                                   │
│  ┌─────────────────┐                          │
│  │ Validate Scores │  Clamp 0.0-1.0           │
│  └────────┬────────┘                          │
│           │                                    │
│           v                                   │
│  ┌─────────────────┐                          │
│  │ Find Bottleneck │  First phase < 0.7       │
│  └────────┬────────┘                          │
│           │                                    │
│           v                                   │
│  ┌─────────────────┐                          │
│  │ Gen Recommendations│  Phase-specific text   │
│  └────────┬────────┘                          │
│           │                                    │
│           v                                   │
│  ┌─────────────────┐                          │
│  │ Score & Level   │  Overall readiness       │
│  └────────┬────────┘                          │
│           │                                    │
│           v                                   │
│  Output: {overall, bottleneck, recommendations}│
└────────────────────────────────────────────────┘
```

**Thresholds:**
- `>= 0.85`: Highly Ready
- `>= 0.65`: Ready
- `>= 0.40`: Partially Ready
- `< 0.40`: Not Ready

**Bottleneck Logic:** The ADKAR model is sequential — you cannot have desire without awareness, or knowledge without desire. The bottleneck is the first phase in sequence that falls below the readiness threshold.

### 5.2 Stakeholder Power/Interest Grid

```
                    HIGH INTEREST
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    │   Keep Informed    │  Manage Closely    │
    │   (Weekly updates, │  (Weekly 1:1,      │
    │    Q&A sessions)   │   co-creation)     │
    │                    │                    │
LOW ─────────────────────┼───────────────────── HIGH
INFLUENCE                │                    INFLUENCE
    │                    │                    │
    │   Monitor          │  Keep Satisfied    │
    │   (Monthly         │  (Bi-weekly exec   │
    │    newsletter)     │   summaries)       │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    LOW INTEREST
```

### 5.3 Communication Channel Matrix

| Phase | Audience | Channel | Frequency | Priority |
|-------|----------|---------|-----------|----------|
| Pre-change | All | Town Hall | One-time | 1 |
| Pre-change | Leaders | Executive Brief | One-time | 1 |
| Awareness | All | Email + Intranet | Weekly | 2 |
| Awareness | Managers | Team Meeting | Weekly | 2 |
| Desire | Individuals | 1-on-1 | As needed | 2 |
| Knowledge | Affected | Workshop | Per module | 1 |
| Ability | Learners | Simulation | Per session | 2 |
| Reinforcement | All | Newsletter | Monthly | 3 |

## 6. Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.10+ | Type hints, dataclasses, enums |
| Data Models | dataclasses | Clean, typed, serializable structures |
| Logging | Python logging | Standard, configurable, level-aware |
| IDs | uuid4 | Collision-resistant, globally unique |
| Time | datetime + timedelta | Native Python datetime handling |
| Serialization | asdict / to_dict | JSON-compatible output |

## 7. Security Considerations

### 7.1 Data Protection
- Stakeholder PII (names, concerns) stored in-memory only
- No persistence to disk without explicit configuration
- Communication content logged at INFO level only

### 7.2 Access Control
- Agent operates in a single-tenant context
- No multi-user isolation (designed for single-operator use)
- Plan data scoped to agent instance lifetime

### 7.3 Audit Trail
- All state changes logged with timestamps
- Stakeholder assessment history maintained
- Resistance interventions tracked with actor attribution

## 8. Scalability

### 8.1 Current Limits
- In-memory storage limits practical plan count to ~100 concurrent plans
- Stakeholder count per plan: ~500 (limited by Python dict performance)
- Training module count: ~1000 per program

### 8.2 Scaling Strategies
- **Database backend**: Replace in-memory stores with PostgreSQL/MongoDB
- **Async processing**: Convert to async/await for concurrent evaluations
- **Microservice decomposition**: Split into independent services per component
- **Caching**: Add Redis for frequently accessed stakeholder/plan data

## 9. Integration Points

```
┌─────────────────┐     ┌──────────────────┐
│ Change Mgmt     │────>│ HR Systems       │
│ Agent           │     │ (Workday, SAP)   │
└────────┬────────┘     └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Communication    │
         │             │ (Slack, Email)   │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ LMS Systems      │
         │             │ (Cornerstone)    │
         │             └──────────────────┘
         │
         └────────────>┌──────────────────┐
                       │ Project Mgmt     │
                       │ (Jira, Asana)    │
                       └──────────────────┘
```

## 10. Error Handling

| Error Type | Handling Strategy |
|-----------|-------------------|
| Invalid stakeholder ID | Return error dict with message |
| Invalid phase in ADKAR | Clamp to valid range, log warning |
| Missing plan reference | Return descriptive error |
| Framework not found | Return available frameworks list |
| Timeline inconsistency | Auto-adjust, log warning |

## 11. Performance

| Metric | Target | Current |
|--------|--------|---------|
| Plan creation | < 100ms | ~50ms |
| Stakeholder assessment | < 50ms | ~20ms |
| ADKAR evaluation | < 30ms | ~15ms |
| Communication plan generation | < 200ms | ~100ms |
| Training program creation | < 150ms | ~75ms |
| Readiness assessment | < 100ms | ~50ms |
| Dashboard generation | < 500ms | ~250ms |

## 12. Testing Strategy

### Unit Tests
- ADKAR evaluator: score clamping, bottleneck detection, threshold logic
- Stakeholder analyzer: grid classification, champion identification
- Resistance manager: intervention plan generation, priority calculation
- Communication planner: template rendering, schedule generation

### Integration Tests
- Full plan creation → stakeholder addition → ADKAR evaluation flow
- Communication plan generation with real stakeholder data
- Training program creation and enrollment cycle
- Readiness assessment with multi-dimensional scoring

### Acceptance Tests
- End-to-end change initiative simulation
- Multi-stakeholder resistance scenario
- Cross-component data consistency validation

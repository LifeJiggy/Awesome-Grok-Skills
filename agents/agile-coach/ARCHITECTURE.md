# AgileCoach Agent Architecture

## Overview

This document describes the architecture for the AgileCoach Agent.

## System Components

```
┌─────────────────────────────────────────┐
│         AgileCoach Agent                    │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Component 1 │  │   Component 2   │  │
│  └─────────────┘  └─────────────────┘  │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Component 3 │  │   Component 4   │  │
│  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────┘
```

## Data Flow

```
Input → Processing → Output
```

## Key Components

### 1. Core Processing

Description of core processing logic.

### 2. Configuration Management

How configuration is handled.

### 3. Integration Layer

How the agent integrates with external systems.

## Configuration

```yaml
config:
  option1: value1
  option2: value2
```

## Performance

| Metric | Value |
|--------|-------|
| Response Time | TBD |
| Throughput | TBD |

## Security Considerations

- Authentication requirements
- Authorization rules
- Data protection measures

## Appendix A: Detailed Component Inventory

### AgileCoachAgent (Orchestrator)

The `AgileCoachAgent` class in `agent.py` coordinates all sub-systems. It owns collections of `Team`, `Sprint`, `Retrospective`, `Improvement`, and `MetricSnapshot` objects. It delegates to helper classes for domain-specific work.

Public surface:
- Team lifecycle: `create_team`, `add_team_member`, `get_team`, `list_teams`
- Ceremonies: `facilitate_retrospective`, `get_retro_template`, `assist_sprint_planning`, `estimate_effort`
- Maturity: `assess_maturity`, `get_assessment_questionnaire`
- Improvements: `create_improvement`, `suggest_improvements`
- Reporting: `get_status`, `generate_report`, `get_history`, `clear_history`
- Integrations: `to_jira_format`, `to_github_format`
- Utilities: `_get_team`, `_generate_retro_id`, `_generate_improvement_id`

### Data Models

All domain entities are `dataclass` instances with `to_dict()` serialization.

- **VelocityRecord**: per-sprint point tracking with capacity and interruption metrics.
- **Retrospective**: links feedback_items, action_items, votes, sentiment, and facilitator metadata.
- **Impediment**: blocker tracking with severity, dependencies, and resolution lifecycle.
- **TeamMember**: role, skills, capacity, timezone, and active status.
- **Team**: aggregates members, velocity_history, impediments, retrospectives, WIP limit, DoD, working agreements.
- **Sprint**: goal, commitment, completion, carryover, scope change, and impediment counts.
- **Improvement**: typed initiatives with effort/impact estimates and retro linkage.
- **MetricSnapshot**: point-in-time metric captures with context.
- **MaturityAssessment**: scored across six dimensions with strengths, weaknesses, and recommendations.
- **Config**: centralized knobs for methodology, reporting formats, caching, concurrency, and integrations.

### Enumerations

- **CeremonyType**: sprint_planning, daily_standup, sprint_review, retrospective, backlog_refinement, pi_planning, scrum_of_scrums
- **Methodology**: scrum, kanban, xp, hybrid, less, safe, crystal, fdd
- **MaturityLevel**: levels 1-5 (Initial → Optimizing)
- **RetrospectiveFormat**: start_stop_continue, mad_sad_glad, sailboat, _4_ls, timeline, fishbone, speedboat, kudos, daki, went_well
- **ImpedimentSeverity**: blocker, high, medium, low
- **ArtifactType**: product_backlog, sprint_backlog, increment, roadmap, vision, burnup/burndown, cfd
- **TeamRole**: product_owner, scrum_master, developer, designer, qa, devops, stakeholder
- **MetricType**: velocity, throughput, lead_time, cycle_time, wip, sprint_burnup, sprint_burndown, cumulative_flow, escaped_defects, team_happiness
- **ImprovementType**: process, technical, communication, tooling, culture, skills, architecture, testing

### MaturityAssessor

Implements a weighted questionnaire across six dimensions:
- technical_practices
- team_collaboration
- delivery
- continuous_improvement
- customer_collaboration
- tooling_automation

Scoring is 1-5 per question. Dimension scores are normalized to 1-5. Overall score maps to MaturityLevel via `_score_to_level`.

The `assess` method returns a `MaturityAssessment` dataclass with truncated strengths, weaknesses, and recommendations (top 5 each).

### SprintPlanner

Plans sprints using:
- Average velocity of last N sprints (configurable window).
- Team capacity = sum(available_hours_per_day × sprint_days for active members).
- Buffer factor (default 0.8) to reduce commitment.
- Risk assessment based on coefficient of variation (CV) of recent velocities.

Returns recommended commitment point value, selected backlog items, and risk level.

### RetrospectiveFacilitator

Supports multiple retrospective formats with templates. Generates prompts based on past action items and team maturity. Produces action items by community voting. Analyzes feedback into themes with category counts and voting scores.

Supported formats include Start/Stop/Continue, Mad/Sad/Glad, Sailboat, 4Ls, Timeline, Fishbone, DAKI, Kudos, Went Well, Speedboat.

### ReportingEngine

Generates multi-format reports (HTML, JSON, CSV). HTML uses inline CSS for a responsive dashboard. JSON embeds full team dicts and computed summary. CSV streams header + rows via `csv.DictWriter`.

### Integration Layer

Transformers convert internal Team state to external tool payloads:
- `to_jira_format`: team name, methodology, maturity, velocity, WIP limit, open impediments
- `to_github_format`: team name, sprint duration, average velocity, member count, working agreement, DoD

### Configuration Management

`Config` dataclass centralizes operational parameters. Classes accept `Optional[Config]` and fall back to `Config()` defaults.

## Appendix B: State Machines

### Team Lifecycle

```
created → populated(members) → active
active → retrospective → improvement_cycle → active
active → assess_maturity → level_up? → active
active → archived
```

### Sprint Lifecycle

```
planned → active → completed
       ↘ cancelled
```

### Impediment Lifecycle

```
open → assigned → resolved
```

### Improvement Lifecycle

```
proposed → in_progress → completed
         ↘ abandoned
```

## Appendix C: Sequence Diagrams

### Team Creation and Member Addition Flow

```
User → AgileCoachAgent: create_team(name, methodology)
AgileCoachAgent → Team: new Team(...)
AgileCoachAgent → User: Team

User → AgileCoachAgent: add_team_member(team_id, name, role)
AgileCoachAgent → Team: _get_team(team_id)
AgileCoachAgent → TeamMember: new TeamMember(...)
AgileCoachAgent → Team: members.append(member)
AgileCoachAgent → User: TeamMember
```

### Sprint Planning and Estimation Flow

```
User → AgileCoachAgent: assist_sprint_planning(team_id, backlog)
AgileCoachAgent → Team: _get_team(team_id)
AgileCoachAgent → SprintPlanner: plan(team, backlog, buffer_factor)
SprintPlanner → Team: average_velocity(velocity_trend_window)
SprintPlanner → Team: _calculate_capacity(team)
SprintPlanner → User: recommendation dict
```

### Retrospective Flow

```
User → AgileCoachAgent: facilitate_retrospective(team_id, fmt)
AgileCoachAgent → Team: _get_team(team_id)
AgileCoachAgent → RetrospectiveFacilitator: generate_action_items(items)
AgileCoachAgent → Team: retrospectives.append(retrospective)
AgileCoachAgent → User: Retrospective
```

### Maturity Assessment Flow

```
User → AgileCoachAgent: assess_maturity(team_id, responses)
AgileCoachAgent → Team: _get_team(team_id)
AgileCoachAgent → MaturityAssessor: assess(team, responses)
MaturityAssessor → Team: team.average_velocity(...)
MaturityAssessor → User: MaturityAssessment
AgileCoachAgent → Team: maturity_level = assessment.level
```

### Report Generation Flow

```
User → AgileCoachAgent: generate_report(team_ids, fmt, output_path)
AgileCoachAgent → Team: list filtered teams
AgileCoachAgent → ReportingEngine: generate(teams, fmt, output_path)
ReportingEngine → User: report content (str)
```

## Appendix D: Data Contracts (JSON Schemas)

### Team

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Team",
  "type": "object",
  "required": ["id", "name", "methodology", "maturity_level", "members", "velocity_history", "impediments", "retrospectives"],
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "methodology": { "type": "string", "enum": ["scrum","kanban","xp","hybrid","less","safe","crystal","fdd"] },
    "maturity_level": { "type": "integer", "minimum": 1, "maximum": 5 },
    "members": { "type": "array", "items": { "$ref": "#/definitions/TeamMember" } },
    "sprint_duration_days": { "type": "integer", "default": 14 },
    "velocity_history": { "type": "array", "items": { "$ref": "#/definitions/VelocityRecord" } },
    "impediments": { "type": "array", "items": { "$ref": "#/definitions/Impediment" } },
    "retrospectives": { "type": "array", "items": { "$ref": "#/definitions/Retrospective" } },
    "wip_limit": { "type": "integer", "default": 5 },
    "definition_of_done": { "type": "array", "items": { "type": "string" } },
    "working_agreement": { "type": "array", "items": { "type": "string" } }
  },
  "definitions": {
    "TeamMember": {
      "type": "object",
      "required": ["id","name","email","role","team_id"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "email": { "type": "string" },
        "role": { "type": "string" },
        "team_id": { "type": "string" },
        "skills": { "type": "array", "items": { "type": "string" } },
        "capacity_points_per_sprint": { "type": "integer", "default": 20 },
        "available_hours_per_day": { "type": "number", "default": 6.0 },
        "timezone": { "type": "string", "default": "UTC" },
        "is_active": { "type": "boolean", "default": true }
      }
    }
  }
}
```

### VelocityRecord

```json
{
  "type": "object",
  "required": ["sprint_id","team_id","committed_points","completed_points","planned_velocity","actual_velocity","start_date","end_date"],
  "properties": {
    "sprint_id": { "type": "string" },
    "team_id": { "type": "string" },
    "committed_points": { "type": "integer" },
    "completed_points": { "type": "integer" },
    "planned_velocity": { "type": "integer" },
    "actual_velocity": { "type": "integer" },
    "start_date": { "type": "string", "format": "date-time" },
    "end_date": { "type": "string", "format": "date-time" },
    "capacity_hours": { "type": "number" },
    "available_hours": { "type": "number" },
    "interruptions_hours": { "type": "number" },
    "context_switches": { "type": "integer" },
    "points_by_type": { "type": "object" },
    "notes": { "type": "string" }
  }
}
```

### Retrospective

```json
{
  "type": "object",
  "required": ["id","team_id","sprint_id","format"],
  "properties": {
    "id": { "type": "string" },
    "team_id": { "type": "string" },
    "sprint_id": { "type": "string" },
    "format": { "type": "string" },
    "feedback_items": { "type": "array", "items": { "type": "object" } },
    "action_items": { "type": "array", "items": { "type": "object" } },
    "votes": { "type": "object", "additionalProperties": { "type": "integer" } },
    "sentiment_score": { "type": "number" },
    "facilitator": { "type": "string" },
    "duration_minutes": { "type": "integer", "default": 60 }
  }
}
```

### Impediment

```json
{
  "type": "object",
  "required": ["id","team_id","description","severity","reported_by","status"],
  "properties": {
    "id": { "type": "string" },
    "team_id": { "type": "string" },
    "description": { "type": "string" },
    "severity": { "type": "string", "enum": ["blocker","high","medium","low"] },
    "reported_by": { "type": "string" },
    "assigned_to": { "type": "string" },
    "status": { "type": "string", "default": "open" },
    "resolution": { "type": "string" },
    "dependencies": { "type": "array", "items": { "type": "string" } }
  }
}
```

### MaturityAssessment

```json
{
  "type": "object",
  "required": ["id","team_id","assessor","assessment_date","overall_score","level","dimension_scores"],
  "properties": {
    "id": { "type": "string" },
    "team_id": { "type": "string" },
    "assessor": { "type": "string" },
    "assessment_date": { "type": "string", "format": "date-time" },
    "overall_score": { "type": "number" },
    "level": { "type": "integer", "minimum": 1, "maximum": 5 },
    "dimension_scores": { "type": "object", "additionalProperties": { "type": "number" } },
    "strengths": { "type": "array", "items": { "type": "string" } },
    "weaknesses": { "type": "array", "items": { "type": "string" } },
    "recommendations": { "type": "array", "items": { "type": "string" } }
  }
}
```

## Appendix E: Configuration Reference

| Config Key | Type | Default | Description |
|------------|------|---------|-------------|
| `default_methodology` | str | `"scrum"` | Default methodology for new teams. |
| `default_sprint_duration_days` | int | `14` | Default sprint length in days. |
| `ceremonies_per_sprint` | int | `5` | Expected ceremony count. |
| `target_maturity_level` | int | `4` | Target maturity for recommendations. |
| `velocity_trend_window` | int | `5` | Number of sprints for moving average. |
| `min_velocity` | int | `5` | Floor for velocity adjustments. |
| `max_velocity` | int | `100` | Ceiling for velocity adjustments. |
| `wip_limit_default` | int | `5` | Default WIP limit for new teams. |
| `enable_retrospectives` | bool | `True` | Toggle retrospective features. |
| `enable_velocity_tracking` | bool | `True` | Toggle velocity tracking. |
| `enable_maturity_assessment` | bool | `True` | Toggle maturity assessment. |
| `enable_impediment_tracking` | bool | `True` | Toggle impediment tracking. |
| `enable_technical_debt_tracking` | bool | `False` | Toggle technical debt tracking. |
| `enable_cfd` | bool | `False` | Toggle cumulative flow diagrams. |
| `report_formats` | List[str] | `["html","json","csv"]` | Export formats. |
| `output_directory` | str | `"./agile_reports"` | Report output path. |
| `history_enabled` | bool | `True` | Enable action history tracking. |
| `history_file` | str | `"agile_coach_history.json"` | History persistence file. |
| `retention_days` | int | `365` | History retention window. |
| `cache_enabled` | bool | `True` | Toggle query/calculation caching. |
| `cache_ttl_hours` | int | `24` | Cache time-to-live. |
| `integrations` | Dict | `{}` | Third-party integration configs. |
| `notification_channels` | List[str] | `["email"]` | Alert channels. |
| `concurrency` | int | `4` | Max parallel async workers. |

## Appendix F: Performance Model

### Complexity Analysis

| Operation | Complexity | Notes |
|-----------|------------|-------|
| `create_team` | O(1) | Appends to internal list. |
| `add_team_member` | O(1) | Appends to team members. |
| `list_teams` | O(T) | T = total teams; optional filters are O(T). |
| `average_velocity` | O(N) | N = velocity records considered. |
| `assess_maturity` | O(D*Q) | D = dimensions, Q = questions per dimension. |
| `plan` (sprint) | O(B) | B = backlog items sorted and filtered. |
| `generate_report` | O(R*C) | R = teams, C = members/records per team. |
| `generate_action_items` | O(F) | F = feedback items. |

### Memory Characteristics

- In-memory only: bounded by number of teams and history depth.
- History list: bounded by `retention_days` or max entries if persisted.
- Caching: bounded by TTL; no eviction policy beyond time.
- No database or queue back-pressure in current implementation.

### Concurrency Model

The `Config.concurrency` parameter hints at async batch use, but the current `agent.py` is synchronous. Production deployments should wrap synchronous calls with a thread pool or transition the engine to async/await patterns if I/O-bound integrations (Jira, GitHub, Azure DevOps) are added.

## Appendix G: Error Handling Strategy

### Exception Hierarchy

```
AgileCoachError (base)
├── TeamError
├── SprintError
├── AssessmentError
├── CeremonyError
└── ConfigurationError
```

Principles:
- Validate inputs early (non-empty names, valid enum values).
- Use domain-specific exceptions to let callers branch on failure type.
- Log with context (team_id, sprint_id) at `logger.error` or `logger.warning`.
- Return safe defaults (e.g., `{}`) for optional external integrations when data is missing.

### Recovery Patterns

- **Idempotent creation**: `create_team` appends a new unique ID each call; callers must deduplicate externally if needed.
- **Graceful degradation**: reporting and integration methods return empty dicts when teams are missing.
- **Validation gates**: `add_team_member` requires a valid `team_id`; raises `TeamError` if not found.

## Appendix H: Monitoring & Observability

### Logging

- Uses standard `logging.getLogger(__name__)`.
- Recommended log levels:
  - `DEBUG`: internal calculations, cache hits, query params.
  - `INFO`: team created, report generated, assessment completed.
  - `WARNING`: cache expiry, missing optional integrations.
  - `ERROR`: failed assertions, invalid configuration, unhandled exceptions.

### Metrics to Track

- Teams created / archived per day.
- Average sprint velocity trend.
- Open impediment count by severity.
- Retrospective sentiment average.
- Maturity level distribution.
- Report generation latency and format mix.
- Cache hit rate.

### Health Checks

- `get_status()` returns team/methodology/impediment counts.
- History depth via `len(get_history())`.
- Feature flags (`enable_*`) confirm active sub-systems.

## Appendix I: Glossary

- **Team**: Top-level agile unit with members, velocity, and rituals.
- **Sprint**: Fixed-duration iteration with goal and commitment.
- **Velocity**: Story points completed per sprint.
- **WIP Limit**: Work-in-progress constraint for flow.
- **DoD**: Definition of Done shared quality checklist.
- **Impediment**: Blocking or slowing issue.
- **Retrospective**: Team reflection ceremony.
- **Maturity Level**: 1-5 scale of agile sophistication.
- **Capacity**: Available person-hours per sprint.
- **Buffer Factor**: Safety multiplier applied to capacity.
- **Coefficient of Variation (CV)**: std / mean, used for risk assessment.
- **Baseline**: Historical average for anomaly comparison.

## Appendix J: Methodology Deep Dive

### Scrum

Iterative sprints, fixed roles (PO, SM, Devs), ceremonies (planning, daily, review, retro), artifacts (backlog, increment, burndown).

### Kanban

Visual board, WIP limits, continuous flow, pull-based, metrics: lead time, cycle time, throughput, cumulative flow diagram.

### XP (Extreme Programming)

Engineering practices: TDD, pair programming, continuous integration, refactoring, small releases, collective ownership.

### LeSS (Large-Scale Scrum)

Multi-team Scrum with single product backlog, shared sprint, unified retrospective, feature teams over component teams.

### SAFe (Scaled Agile Framework)

Agile release trains (ARTs), PI planning, program and team-level Kanban, epics → capabilities → features → stories hierarchy.

### Crystal

Family of methodologies; color indicates criticality (Clear, Yellow, Orange, Red, Diamond). Emphasizes people, interaction, community, and skills over processes.

### FDD (Feature-Driven Development)

Five processes: develop overall model, build feature list, plan by feature, design by feature, build by feature. Domain-driven with chief programmers.

### Hybrid

Blends Scrum cadence with Kanban WIP management and XP engineering practices. Configurable via `Methodology.HYBRID`.

## Appendix K: Maturity Models Reference

### CMMI Comparison

| AgileCoach Level | CMMI Equivalent | Focus |
|------------------|-----------------|-------|
| 1 Initial | Initial | Ad-hoc, unpredictable. |
| 2 Managed | Managed | Project planning and tracking. |
| 3 Defined | Defined | Organization-wide standards. |
| 4 Measured | Quantitatively Managed | Metrics-driven. |
| 5 Optimizing | Optimizing | Continuous improvement. |

### Questionnaires by Dimension

Each dimension in `MaturityAssessor` contains 5 questions with weights 0.5-1.0. Scoring 1-5 per question. Dimension score = weighted average normalized to 5-point scale.

## Appendix L: Retrospective Formats Catalog

### Start/Stop/Continue

Columns: Start, Stop, Continue. Best for: behavioral changes.

### Mad/Sad/Glad

Columns: Mad, Sad, Glad. Best for: emotional team dynamics.

### Sailboat

Columns: Wind (drivers), Anchor (drag), Island (goal), Rocks (risks). Best for: goal alignment.

### 4Ls

Columns: Liked, Learned, Lacked, Longed For. Best for: learning-focused retrospectives.

### Timeline

Map highs/lows across the sprint on a timeline. Best for: event-driven analysis.

### Fishbone (Ishikawa)

Categories: People, Process, Tools, Management, Requirements, Environment. Best for: root cause analysis.

### DAKI

Columns: Drop, Add, Keep, Improve. Best for: prioritization.

### Speedboat

Columns: Engine (propellers), Anchor (drag), Island (destination), Rocks (risks). Similar to Sailboat.

### Kudos

Focused on appreciation. Best for: team morale.

### Went Well

Single-column focus on positives. Best for: celebrating wins.

## Appendix M: Integration Guide

### Jira Integration

`to_jira_format(team_id)` returns a payload compatible with Jira issue metadata. Example transformation to create Epic/Story links:

```python
payload = agent.to_jira_format(team_id)
# Map payload["team"] → Jira project key
# Map payload["impediments"] → Jira blockers
```

### GitHub Integration

`to_github_format(team_id)` returns a payload with working agreement and DoD that can be stored in a repository wiki or issue template.

### Azure DevOps (Placeholder)

Extend integration hooks by:
1. Adding `to_azure_devops_format(self, team_id)` return dict.
2. Updating `Config.integrations` with instance URL and PAT.

## Appendix N: Data Retention & Compliance

- History entries are timestamped ISO8601.
- `retention_days` defines soft TTL; production should implement a cleanup job.
- No PII encryption at rest in the current implementation.
- Reports written to `output_directory` should be protected by filesystem ACLs or token-scoped storage (S3 presigned URLs, etc.).

## Appendix O: Performance Tuning

- Reduce `velocity_trend_window` to 3 for faster adaptation at the cost of stability.
- Increase `max_velocity`/`min_velocity` bounds to limit constraint checks.
- Use `report_formats = ["json"]` for machine consumption.
- Disable `history_enabled` in high-throughput batch scenarios.
- Set `concurrency` to match I/O concurrency of downstream integrations.

## Appendix P: FAQ

**Q: Can multiple methodologies run in one team?**
A: The agent supports one `Methodology` per `Team`. Use `HYBRID` for blended practices.

**Q: How is capacity calculated?**
A: Sum of `available_hours_per_day × sprint_duration_days` for all active members.

**Q: Does maturity assessment require external data?**
A: No. It uses questionnaire responses passed by the caller.

**Q: Can I persist state?**
A: Current implementation is in-memory. Persist by serializing `team.to_dict()` and reloading into a fresh agent instance.

**Q: How do I integrate with Jira?**
A: Use `to_jira_format()` and map returned dict to your Jira REST API payload.

## Appendix Q: Migration Guide

### From v0.x Script-Based Coaching

- Replace procedural script calls with `AgileCoachAgent` methods.
- Enumerate entities into dataclasses before passing to the agent.
- Persist team state externally; agent does not auto-save.

### From External Maturity Tools

- Align your questionnaire to the 30-question, 6-dimension model in `MaturityAssessor`.
- Map scores 1-5 per question to the agent's expected `responses` dict.

## Appendix R: Bibliography & References

- Scrum Guide (2020): https://scrumguides.org
- Kanban Guide: https://kanban.university
- XP Practices: https:// extremeprogramming.org
- LeSS: https://less.works
- SAFe: https://scaledagileframework.com
- CMMI: https://cmmiinstitute.com
- Agile Practice Guide (PMI): https://www.pmi.org/agile

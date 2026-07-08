# AgileCoach Agent

Agile Coach Agent - Team Guidance and Methodology.

## Quick Start

```python
from agents.agile-coach.agent import AgileCoachAgent

agent = AgileCoachAgent()
result = agent.run()
print(result)
```

## Run the Agent

```bash
python agents/agile-coach/agent.py
```

## Files

- `agent.py` - Main implementation
- `GROK.md` - Agent instructions
- `ARCHITECTURE.md` - System architecture
- `README.md` - This file

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Core Concepts](#core-concepts)
7. [API Reference](#api-reference)
8. [Usage Patterns](#usage-patterns)
9. [Ceremonies](#ceremonies)
10. [Sprint Management](#sprint-management)
11. [Retrospectives](#retrospectives)
12. [Team Maturity Assessment](#team-maturity-assessment)
13. [Improvements](#improvements)
14. [Metrics & Dashboards](#metrics--dashboards)
15. [Reporting](#reporting)
16. [Integration Hooks](#integration-hooks)
17. [Performance Tuning](#performance-tuning)
18. [Security & Privacy](#security--privacy)
19. [Extending the Agent](#extending-the-agent)
20. [Troubleshooting](#troubleshooting)
21. [FAQ](#faq)
22. [Contributing](#contributing)

---

## Overview

The AgileCoach Agent is a comprehensive coaching and team-assessment platform. It is designed to be:

- **Methodology-agnostic**: scrum, kanban, XP, LeSS, SAFe, crystal, fdd, hybrid.
- **Metrics-driven**: built-in velocity, WIP, lead time, cycle time, cumulative flow, team happiness.
- **Actionable**: generatessuggestions, action items, and maturity recommendations.
- **Extensible**: add custom methodologies, ceremonies, metrics, and integrations.

### What It Does

- Creates and manages agile teams with members, capacity, and working agreements.
- Facilitates ceremonies (sprint planning, retrospectives, PI planning).
- Tracks velocity, impediments, and sprint health.
- Assesses team maturity across six dimensions.
- Generates action items from retrospective feedback.
- Produces HTML, JSON, and CSV team reports.
- Integrates with Jira and GitHub.

---

## Key Features

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Team Management** | Create teams, add members, set methodology, capacity, maturity. |
| **Sprint Planning** | Capacity-based commitment forecasting with buffer factor. |
| **Retrospectives** | Multi-format facilitation with voting and action item generation. |
| **Maturity Assessment** | 6-dimension questionnaire with weighted scoring and recommendations. |
| **Velocity Tracking** | Per-sprint point tracking, moving averages, trend windows. |
| **Impediment Management** | Track blockers with severity, dependencies, and resolution lifecycle. |
| **Reporting** | HTML, JSON, CSV exports with team summaries and metric breakdowns. |
| **Integrations** | Jira-compatible payloads, GitHub-compatible payloads. |

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

Optional dependencies:
```bash
pip install pandas numpy  # advanced metrics
pip install matplotlib  # custom chart export
pip install jira  # direct Jira API integration
pip install requests  # webhook dispatch
```

---

## Configuration

```python
from agents.agile-coach.agent import AgileCoachAgent, Config, Methodology

config = Config(
    default_methodology="scrum",
    default_sprint_duration_days=14,
    target_maturity_level=4,
    velocity_trend_window=5,
    min_velocity=5,
    max_velocity=100,
    wip_limit_default=5,
    enable_retrospectives=True,
    enable_velocity_tracking=True,
    enable_maturity_assessment=True,
    enable_impediment_tracking=True,
    enable_technical_debt_tracking=False,
    enable_cfd=False,
    report_formats=["html", "json", "csv"],
    output_directory="./agile_reports",
    history_enabled=True,
    retention_days=365,
    cache_enabled=True,
    cache_ttl_hours=24,
    integrations={},
    notification_channels=["email"],
    concurrency=4,
)

agent = AgileCoachAgent(config=config)
team = agent.create_team(
    name="Platform Alpha",
    methodology=Methodology.SCRUM.value,
    sprint_duration_days=14,
)
```

---

## Core Concepts

### Team Entities

| Entity | Description |
|--------|-------------|
| **Team** | Top-level unit with members, velocity, impediments, retrospectives. |
| **TeamMember** | Person with role, skills, capacity, timezone. |
| **Sprint** | Iteration with goal, commitment, completion, carryover. |
| **VelocityRecord** | Per-sprint committed/completed points and capacity. |
| **Retrospective** | Feedback, action items, votes, sentiment. |
| **Impediment** | Blockers with severity, dependencies, resolution. |
| **Improvement** | Tracked initiatives linked to retrospectives. |
| **MetricSnapshot** | Point-in-time metric capture with context. |
| **MaturityAssessment** | Dimensioned score with strengths, weaknesses, recommendations. |

### Methodologies

| Methodology | Characteristics |
|-------------|-----------------|
| **Scrum** | Fixed sprints, ceremonies, roles. |
| **Kanban** | Continuous flow, WIP limits, pull-based. |
| **XP** | TDD, pair programming, CI/CD, refactoring. |
| **Hybrid** | Scrum cadence + Kanban WIP + XP engineering. |
| **LeSS** | Multi-team Scrum, shared backlog, unified retro. |
| **SAFe** | ARTs, PI planning, program backlog, epics. |
| **Crystal** | Color-coded criticality, people-first. |
| **FDD** | Feature-focused, domain-driven, five processes. |

### Maturity Levels

| Level | Name | Typical Characteristics |
|-------|------|------------------------|
| 1 | Initial | Ad-hoc, unpredictable delivery. |
| 2 | Managed | Basic planning and tracking. |
| 3 | Defined | Organization-wide standards. |
| 4 | Measured | Metrics-driven decisions. |
| 5 | Optimizing | Continuous improvement culture. |

---

## API Reference

### AgileCoachAgent

- `create_team(name, methodology="scrum", sprint_duration_days=14) -> Team`
- `add_team_member(team_id, name, role, email="", skills=None) -> TeamMember`
- `get_team(team_id) -> Optional[Team]`
- `list_teams(methodology=None, maturity_level=None) -> List[Team]`
- `facilitate_retrospective(team_id, fmt="start_stop_continue", feedback_items=None, facilitator="AgileCoachAgent", duration_minutes=60) -> Retrospective`
- `get_retro_template(fmt) -> Dict[str, Any]`
- `assist_sprint_planning(team_id, backlog, buffer_factor=0.8) -> Dict[str, Any]`
- `estimate_effort(items) -> Dict[str, Any]`
- `assess_maturity(team_id, responses, assessor="AgileCoachAgent") -> MaturityAssessment`
- `get_assessment_questionnaire() -> Dict[str, List[Dict[str, Any]]]`
- `create_improvement(team_id, improvement_type, title, description, priority="medium") -> Improvement`
- `suggest_improvements(team_id) -> List[str]`
- `get_status() -> Dict[str, Any]`
- `generate_report(team_ids=None, fmt="html", output_path=None) -> str`
- `get_history() -> List[Dict[str, Any]]`
- `clear_history() -> None`
- `to_jira_format(team_id) -> Dict[str, Any]`
- `to_github_format(team_id) -> Dict[str, Any]`

### Supporting Classes

- `MaturityAssessor(config)`: dimensioned scoring engine.
- `SprintPlanner(config)`: capacity-aware commitment planning.
- `RetrospectiveFacilitator(config)`: template and action item generation.
- `ReportingEngine(config)`: HTML/JSON/CSV rendering.

---

## Usage Patterns

### Pattern 1: Team Bootstrap

```python
agent = AgileCoachAgent()
team = agent.create_team("Alpha", Methodology.SCRUM.value)
agent.add_team_member(team.id, "Alice", TeamRole.DEVELOPER.value, skills=["python","sql"])
agent.add_team_member(team.id, "Bob", TeamRole.DESIGNER.value, skills=["figma","ux"])
```

### Pattern 2: Sprint Planning with Backlog

```python
backlog = [
    {"id": "US-001", "title": "Login flow", "story_points": 5, "priority": 1},
    {"id": "US-002", "title": "Dashboard", "story_points": 8, "priority": 2},
]
plan = agent.assist_sprint_planning(team.id, backlog, buffer_factor=0.8)
print(f"Recommended commitment: {plan['recommended_commitment']} points")
```

### Pattern 3: Retrospective and Action Items

```python
feedback = [
    {"category": "process", "text": "Standups run long", "votes": 4},
    {"category": "tooling", "text": "CI is flaky", "votes": 3},
]
retro = agent.facilitate_retrospective(team.id, fmt="start_stop_continue", feedback_items=feedback)
print(f"Action items: {[a['title'] for a in retro.action_items]}")
```

### Pattern 4: Maturity Assessment

```python
responses = {f"q{i}": 3 for i in range(1, 31)}
assessment = agent.assess_maturity(team.id, responses)
print(f"Level: {assessment.level.name}, Score: {assessment.overall_score:.1f}")
```

### Pattern 5: Reporting and Export

```python
report = agent.generate_report(fmt="json", output_path="./alpha_team_report.json")
```

### Pattern 6: Suggest Improvements

```python
for suggestion in agent.suggest_improvements(team.id):
    print(f"- {suggestion}")
```

---

## Ceremonies

### Supported Ceremony Types

| Type | Description |
|------|-------------|
| **sprint_planning** | Commitment and backlog selection. |
| **daily_standup** | 15-minute sync. |
| **sprint_review** | Demo and stakeholder feedback. |
| **retrospective** | Team reflection and action items. |
| **backlog_refinement** | Story grooming and estimation. |
| **pi_planning** | Program increment coordination. |
| **scrum_of_scrums** | Cross-team coordination. |

### Retrospective Formats

| Format | Columns | Best For |
|--------|---------|----------|
| **start_stop_continue** | Start / Stop / Continue | Behavioral change |
| **mad_sad_glad** | Mad / Sad / Glad | Emotional dynamics |
| **sailboat** | Wind / Anchor / Island / Rocks | Goal alignment |
| **4_ls** | Liked / Learned / Lacked / Longed For | Learning focus |
| **timeline** | Chronological | Event-driven analysis |
| **fishbone** | Root categories | Root cause analysis |
| **speedboat** | Engine / Anchor / Island / Rocks | Alternative sailboat |
| **kudos** | Appreciation | Team morale |
| **daki** | Drop / Add / Keep / Improve | Prioritization |
| **went_well** | Positives only | Celebration |

---

## Sprint Management

### Planning Workflow

1. Gather team capacity (members × days × hours/day).
2. Compute buffer-adjusted commitment using average velocity.
3. Sort backlog by priority, select items within commitment.
4. Assess risk using coefficient of variation of recent velocities.

### Velocity Tracking Fields

- `committed_points`: planned for sprint.
- `completed_points`: delivered.
- `planned_velocity`: planned points from previous planning.
- `actual_velocity`: actual completed points.
- `capacity_hours` / `available_hours`: capacity accounting.
- `interruptions_hours` / `context_switches`: focus loss metrics.

### Risk Levels

| CV | Risk | Interpretation |
|----|------|----------------|
| < 0.2 | low | Highly predictable team. |
| < 0.5 | medium | Moderate variability. |
| >= 0.5 | high | Unpredictable; lower commitment advised. |

---

## Team Maturity Assessment

### Dimensions Assessed

| Dimension | Sample Questions |
|-----------|-----------------|
| **Technical Practices** | CI, test coverage, code reviews, refactoring, pair programming. |
| **Team Collaboration** | Cross-functional, self-organization, T-shaped skills, psychological safety. |
| **Delivery** | CI/CD deploy frequency, lead time, velocity predictability, incident rate. |
| **Continuous Improvement** | Retro frequency, action item follow-through, experimentation, blameless post-mortems. |
| **Customer Collaboration** | PO availability, backlog refinement, acceptance criteria, stakeholder attendance. |
| **Tooling/Automation** | Issue repo integration, monitoring, chatops, documentation automation. |

### Scoring Rules

- Answers are 1-5 per question.
- Each question has a weight 0.5-1.0.
- Dimension score = weighted average normalized to 5-point scale.
- Overall score = arithmetic mean of dimension scores.
- Level mapping:
  - 4.5+ → Level 5 Optimizing
  - 3.5+ → Level 4 Measured
  - 2.5+ → Level 3 Defined
  - 1.5+ → Level 2 Managed
  - < 1.5 → Level 1 Initial

---

## Improvements

### Improvement Types

- process, technical, communication, tooling, culture, skills, architecture, testing

### Suggestion Rules

The agent suggests improvements when:
- Definition of Done is empty.
- Maturity level < 3.
- Average velocity below `min_velocity`.
- Working agreement is empty.
-More than 3 open impediments.

### Tracking Lifecycle

proposed → in_progress → completed / abandoned

---

## Metrics & Dashboards

### Built-in Metrics

| Metric | Description |
|--------|-------------|
| **velocity** | Story points completed per sprint. |
| **throughput** | Items completed per unit time. |
| **lead_time** | Request to delivery duration. |
| **cycle_time** | Active work duration. |
| **wip** | Work-in-progress items in progress. |
| **sprint_burnup** | Remaining work chart. |
| **sprint_burndown** | Remaining effort chart. |
| **cumulative_flow** | WIP state distribution chart. |
| **escaped_defects** | Defects found post-release. |
| **team_happiness** | Subjective team morale. |

---

## Reporting

### Output Formats

| Format | Use Case |
|--------|----------|
| **html** | Human-readable dashboard. |
| **json** | Machine-readable, API-friendly. |
| **csv** | Spreadsheet export for BI tools. |

### Report Contents (HTML)

- Summary cards: total teams, total members, open impediments, high maturity count.
- Team details table: methodology, maturity, members, avg velocity, impediments, retros.
- Inline CSS for responsive layout.

### Report Contents (JSON)

```json
{
  "generated_at": "ISO8601",
  "teams": [...],
  "summary": {
    "total_teams": 0,
    "total_members": 0,
    "avg_velocity": 0.0,
    "avg_maturity": 0.0
  }
}
```

### Report Contents (CSV)

Columns: id, name, methodology, maturity_level, members, avg_velocity, impediments, retros.

---

## Integration Hooks

### Jira Format

```python
payload = agent.to_jira_format(team_id)
# team, methodology, maturity, velocity, wip_limit, open_impediments
```

### GitHub Format

```python
payload = agent.to_github_format(team_id)
# team, sprint_duration_days, average_velocity, members, working_agreement, definition_of_done
```

### Custom Integration

Extend by:
1. Adding a transformation method to `AgileCoachAgent`.
2. Storing credentials in `Config.integrations`.
3. Calling the method from CI or chatops.

---

## Performance Tuning

- Limit `velocity_trend_window` to reduce computation per request.
- Disable `history_enabled` in batch or agent environments.
- Use `report_formats = ["json"]` for low-latency exports.
- Cache maturity assessments if the questionnaire is static.

---

## Security & Privacy

- No secrets stored in `Team`, `Config`, or report outputs by default.
- Integrations should use environment-scoped credentials.
- Restrict access to `output_directory`; consider secrets management (Vault, env vars).
- Avoid logging member emails at INFO level.

---

## Extending the Agent

### Custom Ceremony Type

Add a value to `CeremonyType` and a corresponding facilitator branch.

### Custom Methodology

Add a value to `Methodology` and handle it in planning/assessment logic.

### Custom Maturity Dimension

Add a key to `MaturityAssessor._build_questionnaire` and include it in dimension scoring.

### Custom Improvement Type

Add to `ImprovementType` enum; extend `suggest_improvements` rules.

### Custom Report Section

Subclass `ReportingEngine` and override `_generate_html` / `_generate_json` / `_generate_csv`.

---

## Troubleshooting

### Problem: Team not found

- Verify `team_id` via `list_teams()` / `get_team()`.
- IDs include timestamp suffixes; persist IDs externally.

### Problem: Maturity score unexpectedly high/low

- Inspect `raw_responses` in `MaturityAssessment`.
- Adjust question weights in `MaturityAssessor._build_questionnaire`.

### Problem: Velocity average does not update

- Ensure `VelocityRecord` instances are appended to `team.velocity_history`.
- Check `velocity_trend_window` is greater than 0.

### Problem: Report generation fails in CSV

- Ensure `team.average_velocity()` returns a value; handle `0.0` division-safe formatting.

### Problem: Retrospective action items empty

- Verify `feedback_items` has entries with `votes > 0`.

---

## FAQ

**Q: Is this production-ready?**
A: The model is production-patterned (typed, structured, recoverable) but uses in-memory state. Add persistence and access controls for production.

**Q: Does it support SAFe?**
A: `Methodology.SAFE` is defined; add PI planning workflows externally.

**Q: Can assessments be automated?**
A: Responses are caller-supplied. Integrate with survey tools to auto-populate.

**Q: How do I reset state?**
A: Create a new `AgileCoachAgent()` or call `clear_history()` plus manual team list reset.

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*AgileCoach Agent - Part of the Awesome Grok Skills collection.*

*"From sprint to scrum mastery."*

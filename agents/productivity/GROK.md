---
name: "Productivity Automation Agent"
version: "1.0.0"
description: "AI-powered productivity optimization and workflow automation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["productivity", "automation", "workflow", "efficiency"]
category: "productivity"
personality: "efficiency-expert"
use_cases: ["workflow automation", "task management", "productivity optimization"]
---

# Productivity Automation Agent

> Maximize human productivity through AI-driven workflow optimization and intelligent automation

## Why This Matters

Grok's efficiency focus and analytical mind create perfect productivity tools:

- **Maximum Efficiency**: Eliminate waste and optimize every process
- **Intelligent Automation**: Smart task delegation and scheduling
- **Physics-Inspired Optimization**: Minimize resistance, maximize flow
- **Real-time Adaptation**: Dynamic workflow adjustment

## Core Capabilities

### 1. Workflow Automation
- Task scheduling: intelligent
- Process optimization: continuous
- Meeting management: automated
- Communication routing: smart
- Documentation: auto-generated

### 2. Time Management
- Focus time: protected
- Task prioritization: ai_driven
- Energy optimization: physics_based
- Break scheduling: optimal
- Performance tracking: real_time

### 3. Knowledge Management
- Information organization: automated
- Search enhancement: intelligent
- Learning optimization: personalized
- Collaboration: seamless
- Knowledge sharing: proactive

## Key Features

### Intelligent Task Management

```python
class ProductivityOptimizer:
    def __init__(self):
        self.productivity_patterns = {
            'morning_person': {'peak_hours': [9, 10, 11], 'deep_work_blocks': 2},
            'afternoon_person': {'peak_hours': [14, 15, 16], 'deep_work_blocks': 2},
            'evening_person': {'peak_hours': [19, 20, 21], 'deep_work_blocks': 1}
        }

    def optimize_schedule(self, tasks, user_profile):
        chronotype = self.identify_chronotype(user_profile)
        analyzed_tasks = []
        for task in tasks:
            task_analysis = {
                'name': task['name'],
                'priority': task['priority'],
                'duration': task['estimated_duration'],
                'complexity': task['complexity'],
                'energy_required': task['energy_required'],
                'collaboration_needed': task.get('collaboration', False),
                'deadline': task.get('deadline')
            }
            analyzed_tasks.append(task_analysis)
        schedule = self.create_optimal_schedule(analyzed_tasks, chronotype, user_profile)
        return {
            'schedule': schedule,
            'productivity_score': self.calculate_productivity_score(schedule),
            'recommendations': self.generate_productivity_recommendations(schedule, user_profile),
            'energy_map': self.create_energy_map(schedule)
        }

    def calculate_flow_state_conditions(self, current_task, environmental_factors):
        challenge_level = current_task['complexity']
        skill_level = current_task['user_skill_level']
        noise_level = environmental_factors['noise']
        temperature = environmental_factors['temperature']
        lighting = environmental_factors['lighting']
        interruptions = environmental_factors['interruptions']

        challenge_skill_ratio = challenge_level / skill_level
        optimal_ratio = 1.0
        ratio_deviation = abs(challenge_skill_ratio - optimal_ratio)

        environment_score = (
            self.calculate_noise_score(noise_level) * 0.3 +
            self.calculate_temperature_score(temperature) * 0.2 +
            self.calculate_lighting_score(lighting) * 0.2 +
            self.calculate_interruption_score(interruptions) * 0.3
        )

        flow_probability = (1 - ratio_deviation) * environment_score

        return {
            'flow_probability': max(0, min(1, flow_probability)),
            'challenge_skill_ratio': challenge_skill_ratio,
            'environmental_factors': {
                'noise_score': self.calculate_noise_score(noise_level),
                'temperature_score': self.calculate_temperature_score(temperature),
                'lighting_score': self.calculate_lighting_score(lighting),
                'interruption_score': self.calculate_interruption_score(interruptions)
            },
            'recommendations': self.generate_flow_recommendations(ratio_deviation, environment_score)
        }
```

### Automated Workflow Integration

```python
class WorkflowAutomator:
    def __init__(self):
        self.automation_rules = {
            'email_processing': self.email_automation_rules,
            'meeting_scheduling': self.meeting_automation_rules,
            'task_delegation': self.delegation_automation_rules,
            'knowledge_capture': self.knowledge_automation_rules
        }

    def create_automation_workflows(self, user_preferences, available_tools):
        workflows = {}

        email_workflow = {
            'name': 'Email Processing Automation',
            'triggers': ['new_email_received'],
            'actions': [
                {
                    'type': 'categorize',
                    'rules': [
                        {'if': 'from:team', 'category': 'internal', 'priority': 'high'},
                        {'if': 'subject:urgent', 'category': 'urgent', 'priority': 'highest'},
                        {'if': 'subject:meeting', 'category': 'calendar', 'action': 'extract_meeting_info'}
                    ]
                },
                {
                    'type': 'auto_reply',
                    'conditions': ['out_of_office', 'vacation_mode'],
                    'template': 'auto_reply_template'
                },
                {
                    'type': 'task_creation',
                    'conditions': ['action_required', 'deadline_mentioned'],
                    'integration': 'task_manager'
                }
            ]
        }
        workflows['email'] = email_workflow

        meeting_workflow = {
            'name': 'Meeting Optimization',
            'triggers': ['meeting_requested', 'meeting_scheduled'],
            'actions': [
                {
                    'type': 'agenda_creation',
                    'template': 'meeting_agenda_template',
                    'participants': 'auto_extract'
                },
                {
                    'type': 'time_optimization',
                    'rules': ['avoid_low_energy_periods', 'consider_time_zones', 'buffer_time']
                },
                {
                    'type': 'follow_up_automation',
                    'trigger': 'meeting_ended',
                    'actions': ['summary_generation', 'action_item_extraction', 'recording_processing']
                }
            ]
        }
        workflows['meetings'] = meeting_workflow

        return {
            'workflows': workflows,
            'integration_map': self.create_integration_map(available_tools),
            'automation_score': self.calculate_automation_score(workflows, user_preferences)
        }
```

## Productivity Analytics

### Performance Tracking

```python
daily_metrics = {
    'deep_work_hours': 4.5,
    'shallow_work_hours': 3.2,
    'meeting_hours': 2.1,
    'break_time': 1.2,
    'interruptions': 8,
    'task_completion_rate': 0.85,
    'energy_level_trend': 'stable',
    'focus_score': 0.78
}

weekly_patterns = {
    'most_productive_day': 'Tuesday',
    'least_productive_day': 'Friday',
    'peak_performance_time': '09:00-11:00',
    'optimal_deep_work_blocks': 2,
    'meeting_efficiency': 0.82,
    'collaboration_vs_focus_ratio': 0.3
}
```

### Optimization Insights

```python
def generate_optimization_insights(metrics, patterns):
    insights = []

    if metrics['deep_work_hours'] < 4:
        insights.append({
            'type': 'deep_work',
            'level': 'warning',
            'message': f"Deep work time below optimal: {metrics['deep_work_hours']} hours",
            'recommendations': [
                'Schedule more deep work blocks',
                'Minimize interruptions during focus time',
                'Use time blocking techniques'
            ],
            'potential_improvement': '+25% productivity'
        })

    if patterns['meeting_efficiency'] < 0.8:
        insights.append({
            'type': 'meetings',
            'level': 'warning',
            'message': f"Meeting efficiency could be improved: {patterns['meeting_efficiency']*100:.1f}%",
            'recommendations': [
                'Implement meeting agendas',
                'Set strict time limits',
                'Use meeting-free days'
            ],
            'potential_improvement': '+15% time availability'
        })

    if metrics['interruptions'] > 10:
        insights.append({
            'type': 'energy',
            'level': 'high',
            'message': f"High interruption rate: {metrics['interruptions']} per day",
            'recommendations': [
                'Implement focus hours',
                'Use batch processing',
                'Configure notification settings'
            ],
            'potential_improvement': '+40% focus score'
        })

    return insights
```

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Task automation framework
- [ ] Basic scheduling optimization
- [ ] Time tracking integration
- [ ] Simple analytics dashboard

### Phase 2: Intelligence (Week 3-4)
- [ ] AI-powered prioritization
- [ ] Flow state optimization
- [ ] Workflow automation
- [ ] Advanced analytics

### Phase 3: Advanced (Week 5-6)
- [ ] Predictive scheduling
- [ ] Energy management
- [ ] Team productivity optimization
- [ ] Cross-platform integration

## Success Metrics

### Productivity Excellence
```yaml
productivity_metrics:
  task_completion_rate: "> 90%"
  deep_work_hours: "> 4 hours/day"
  meeting_efficiency: "> 85%"
  interruption_reduction: "-60%"

time_management:
  scheduling_optimization: "> 80%"
  focus_time_increase: "+40%"
  energy_utilization: "> 85%"
  work_life_balance: "9/10"

automation_impact:
  manual_tasks_reduced: "-70%"
  time_saved: "+15 hours/week"
  error_reduction: "-80%"
  user_satisfaction: "> 4.5/5"
```

---

---

## Task Management Deep Dive

### Priority Matrix

```python
# Eisenhower Matrix for task prioritization
def prioritize_tasks(tasks):
    """Classify tasks by urgency and importance."""

    matrix = {
        "do_first": [],    # Urgent + Important
        "schedule": [],    # Not Urgent + Important
        "delegate": [],    # Urgent + Not Important
        "eliminate": [],   # Not Urgent + Not Important
    }

    for task in tasks:
        if task.urgent and task.important:
            matrix["do_first"].append(task)
        elif not task.urgent and task.important:
            matrix["schedule"].append(task)
        elif task.urgent and not task.important:
            matrix["delegate"].append(task)
        else:
            matrix["eliminate"].append(task)

    return matrix

# Example usage
tasks = agent.tasks.get_all()
prioritized = prioritize_tasks(tasks)

print("Do First (Urgent + Important):")
for task in prioritized["do_first"]:
    print(f"  - {task.title} (deadline: {task.deadline})")

print("\nSchedule (Important, Not Urgent):")
for task in prioritized["schedule"]:
    print(f"  - {task.title}")
```

### Pomodoro Configuration

```python
# Custom Pomodoro settings
agent.pomodoro.configure(
    focus_duration=25,           # minutes
    short_break_duration=5,      # minutes
    long_break_duration=15,      # minutes
    sessions_before_long_break=4,
    daily_target_hours=4,        # 16 pomodoros
    auto_start_breaks=True,
    auto_start_pomodoros=False,
    notification_sound="gentle_chime",
    interruption_handling="log_and_continue",
)
```

### Habit Streak Dashboard

```python
# View habit streaks
dashboard = agent.habits.dashboard()

print("Habit Streaks:")
print("Habit              | Current | Longest | Completion Rate")
print("-" * 55)
for habit in dashboard["habits"]:
    print(f"{habit['name']:19s} | {habit['current_streak']:7d} | {habit['longest_streak']:7d} | {habit['completion_rate']:.1f}%")

print(f"\nOverall Consistency: {dashboard['overall_consistency']:.1f}%")
print(f"Best Day: {dashboard['best_day']}")
print(f"Worst Day: {dashboard['worst_day']}")
```

---

## Calendar Optimization

### Time Blocking Strategy

```python
# Optimize calendar with time blocks
optimized = agent.calendar.optimize(
    tasks=agent.tasks.get_incomplete(),
    energy_pattern=agent.energy.daily_pattern(),
    preferences={
        "deep_work_blocks": [
            {"start": "09:00", "end": "11:00", "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]},
        ],
        "meeting_windows": [
            {"start": "14:00", "end": "16:00", "days": ["monday", "wednesday", "friday"]},
        ],
        "break_duration": 15,  # minutes between meetings
        "lunch_break": {"start": "12:00", "end": "13:00"},
    },
)

print("Optimized Schedule:")
for block in optimized["blocks"]:
    print(f"  {block['start']}-{block['end']}: {block['activity']}")
```

---

## Goal Setting Framework

### SMART Goal Examples

```python
# Create SMART goals
goals = [
    {
        "specific": "Increase daily active users",
        "measurable": "from 1000 to 1500",
        "achievable": "Based on 15% monthly growth rate",
        "relevant": "Aligns with company growth OKR",
        "time_bound": "by end of Q2 2024",
        "target_date": "2024-06-30",
        "current_value": 1000,
        "target_value": 1500,
    },
    {
        "specific": "Reduce customer support tickets",
        "measurable": "from 500 to 300 per week",
        "achievable": "Through better documentation and onboarding",
        "relevant": "Improves customer satisfaction",
        "time_bound": "within 3 months",
        "target_date": "2024-09-30",
        "current_value": 500,
        "target_value": 300,
    },
]

for goal in goals:
    result = agent.goals.create_goal(**goal)
    print(f"Created goal: {result.goal_id}")
    print(f"  Progress needed: {((goal['target_value'] - goal['current_value']) / goal['current_value'] * 100):.1f}%")
```

---

## Time Tracking Analytics

### Weekly Time Analysis

```python
# Analyze time distribution
weekly = agent.time.weekly_summary()

print("Weekly Time Distribution:")
print("=" * 50)
total_hours = sum(weekly.values())
for category, hours in sorted(weekly.items(), key=lambda x: -x[1]):
    percentage = (hours / total_hours) * 100
    bar = "█" * int(percentage / 5)
    print(f"  {category:20s}: {hours:5.1f}h ({percentage:4.1f}%) {bar}")

print(f"\n  {'Total':20s}: {total_hours:5.1f}h")
print(f"  Deep Work Ratio: {weekly.get('deep_work', 0) / total_hours * 100:.1f}%")
```

### Focus Score Calculation

```python
def calculate_focus_score(time_entries):
    """
    Calculate focus score based on:
    - Uninterrupted work duration
    - Task completion rate
    - Energy level alignment
    - Interruption count
    """
    total_focus_time = 0
    total_interruptions = 0
    tasks_completed = 0

    for entry in time_entries:
        if entry.focus_mode == "deep_work":
            total_focus_time += entry.duration
            total_interruptions += entry.interruptions
            if entry.task_completed:
                tasks_completed += 1

    # Focus score formula
    duration_score = min(total_focus_time / 240, 1.0)  # 4 hours = perfect
    interruption_penalty = max(0, 1.0 - (total_interruptions * 0.1))
    completion_rate = tasks_completed / max(len(time_entries), 1)

    focus_score = (duration_score * 0.4 + interruption_penalty * 0.3 + completion_rate * 0.3) * 100

    return {
        "focus_score": round(focus_score, 1),
        "deep_work_hours": round(total_focus_time / 60, 1),
        "interruptions": total_interruptions,
        "completion_rate": round(completion_rate * 100, 1),
    }
```

---

## Habit Formation Science

### Habit Loop Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Habit Loop                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │  Cue    │───►│ Routine │───►│ Reward  │───►│ Craving │ │
│  │         │    │         │    │         │    │         │ │
│  │ Trigger │    │ Action  │    │ Benefit │    │ Desire  │ │
│  │ to act  │    │ to take │    │ to seek │    │ to do   │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘ │
│       │                                              │      │
│       └──────────────────────────────────────────────┘      │
│                                                              │
│  Implementation Intentions:                                  │
│  "When [CUE], I will [ROUTINE] in order to [REWARD]"        │
│                                                              │
│  Example:                                                    │
│  "When I sit at my desk (cue), I will start a pomodoro      │
│   (routine) in order to feel productive (reward)"           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Habit Stacking

```python
# Create habit stacks for better consistency
habit_stack = agent.habits.create_stack(
    name="Morning Productivity Stack",
    habits=[
        {"name": "Hydrate", "duration": 2, "cue": "wake_up"},
        {"name": "Review goals", "duration": 5, "cue": "hydration_done"},
        {"name": "Plan day", "duration": 10, "cue": "goals_reviewed"},
        {"name": "First pomodoro", "duration": 25, "cue": "day_planned"},
        {"name": "Log progress", "duration": 5, "cue": "pomodoro_done"},
    ],
)

print("Morning Stack:")
for i, habit in enumerate(habit_stack.habits):
    print(f"  {i+1}. {habit['name']} ({habit['duration']} min)")
```

---

## Decision Journal

### Structured Decision Logging

```python
# Log a decision with full context
decision = agent.decisions.log(
    title="Switch from MongoDB to PostgreSQL",
    context="Our query patterns have changed from document-centric to relational.",
    options_considered=[
        {"name": "Stay with MongoDB", "pros": ["No migration needed"], "cons": ["Poor join performance"]},
        {"name": "Migrate to PostgreSQL", "pros": ["Better query performance", "ACID compliance"], "cons": ["Migration effort", "Team learning curve"]},
        {"name": "Use both (polyglot)", "pros": ["Best of both"], "cons": ["Operational complexity"]},
    ],
    decision="Migrate to PostgreSQL",
    reasoning="Query performance is critical for our analytics features. Migration effort is manageable with our team size.",
    expected_outcome="50% improvement in query performance for complex reports",
    confidence=0.7,
    decision_date=datetime.now(),
    review_date=datetime.now() + timedelta(days=90),
)

# Review decision outcomes
review = agent.decisions.review(decision.decision_id, actual_outcome="Query performance improved by 65%", lessons_learned="Migration took 2 weeks longer than expected")
```

---

## Integration Patterns

### Calendar Sync

```python
# Sync with external calendars
agent.calendar.sync(
    provider="google",
    credentials="path/to/credentials.json",
    sync_direction="bidirectional",
    sync_interval_minutes=15,
    conflict_resolution="calendar_wins",
)

# Import events from calendar
events = agent.calendar.get_events(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7),
)

for event in events:
    print(f"{event.start_time} - {event.end_time}: {event.title}")
```

### Slack Integration

```python
# Configure Slack notifications
agent.integrations.configure_slack(
    webhook_url="https://hooks.slack.com/services/xxx",
    channel="#productivity",
    notify_on=[
        "pomodoro_complete",
        "habit_streak_milestone",
        "goal_achieved",
        "daily_summary",
    ],
)

# Send productivity summary to Slack
agent.integrations.send_slack_summary(
    include=[
        "tasks_completed",
        "focus_hours",
        "habit_streaks",
        "energy_levels",
    ],
)
```

### GitHub Integration

```python
# Track development time against GitHub issues
agent.integrations.configure_github(
    token="ghp_xxx",
    repository="org/repo",
    auto_link_commits=True,
    track_pr_time=True,
)

# Get development metrics
dev_metrics = agent.integrations.get_github_metrics(
    period="last_30_days",
)

print(f"Development Metrics:")
print(f"  Commits: {dev_metrics['commits']}")
print(f"  PRs Merged: {dev_metrics['prs_merged']}")
print(f"  Issues Closed: {dev_metrics['issues_closed']}")
print(f"  Avg PR Review Time: {dev_metrics['avg_review_time']} hours")
```

---

## Energy Management Deep Dive

### Energy Level Definitions

```python
# Define energy levels with specific characteristics
energy_levels = {
    "PEAK": {
        "description": "Maximum cognitive function",
        "best_for": ["complex problem solving", "creative work", "strategic thinking"],
        "avoid": ["routine tasks", "meetings", "email"],
        "duration": "2-3 hours",
        "recovery": "4-6 hours",
    },
    "HIGH": {
        "description": "Strong performance capacity",
        "best_for": ["focused work", "learning new skills", "collaborative tasks"],
        "avoid": ["deep creative work", "long meetings"],
        "duration": "3-4 hours",
        "recovery": "3-4 hours",
    },
    "MEDIUM": {
        "description": "Normal operational capacity",
        "best_for": ["routine tasks", "meetings", "email", "planning"],
        "avoid": ["complex problem solving", "creative work"],
        "duration": "4-6 hours",
        "recovery": "2-3 hours",
    },
    "LOW": {
        "description": "Reduced cognitive function",
        "best_for": ["simple tasks", "organizing", "low-stakes decisions"],
        "avoid": ["important decisions", "creative work", "meetings"],
        "duration": "2-3 hours",
        "recovery": "3-4 hours",
    },
    "DEPLETED": {
        "description": "Minimal effective capacity",
        "best_for": ["rest", "light reading", "walking"],
        "avoid": ["all work tasks"],
        "duration": "N/A",
        "recovery": "8+ hours sleep",
    },
}
```

### Energy Optimization Recommendations

```python
# Get personalized energy optimization recommendations
recommendations = agent.energy.get_recommendations(
    current_level=agent.energy.get_current_level(),
    tasks=agent.tasks.get_incomplete(),
    calendar=agent.calendar.get_today(),
)

print("Energy Optimization Recommendations:")
for rec in recommendations:
    print(f"\n  [{rec['priority'].upper()}] {rec['title']}")
    print(f"  {rec['description']}")
    if rec.get('action'):
        print(f"  Action: {rec['action']}")
```

---

## Workflow Automation Deep Dive

### Trigger Types

```python
# Define automation triggers
triggers = {
    "time_based": {
        "description": "Trigger at specific times",
        "examples": ["daily at 9am", "every hour", "weekdays only"],
        "cron_expression": "0 9 * * 1-5",
    },
    "event_based": {
        "description": "Trigger on specific events",
        "examples": ["task completed", "meeting ended", "habit logged"],
        "event_types": ["task.completed", "meeting.ended", "habit.logged"],
    },
    "condition_based": {
        "description": "Trigger when conditions are met",
        "examples": ["focus score < 50", "tasks > 10", "streak = 7"],
        "condition_types": ["metric_threshold", "count_threshold", "streak_milestone"],
    },
    "manual": {
        "description": "Trigger on demand",
        "examples": ["button click", "voice command", "shortcut"],
        "integration_types": ["slack_command", "keyboard_shortcut", "voice_assistant"],
    },
}
```

### Automation Templates

```python
# Pre-built automation templates
templates = {
    "morning_routine": {
        "name": "Morning Productivity Setup",
        "triggers": [{"type": "time", "time": "08:00"}],
        "actions": [
            {"type": "show_daily_summary"},
            {"type": "start_pomodoro", "task": "MIT"},
            {"type": "send_notification", "message": "Good morning! Ready to be productive?"},
        ],
    },
    "end_of_day": {
        "name": "Daily Shutdown",
        "triggers": [{"type": "time", "time": "17:30"}],
        "actions": [
            {"type": "stop_all_timers"},
            {"type": "log_daily_summary"},
            {"type": "plan_tomorrow"},
            {"type": "send_notification", "message": "Great work today! See you tomorrow."},
        ],
    },
    "meeting_prep": {
        "name": "Meeting Preparation",
        "triggers": [{"type": "time_offset", "minutes_before": 15}],
        "actions": [
            {"type": "show_agenda"},
            {"type": "show_participant_info"},
            {"type": "set_status", "status": "In Meeting"},
        ],
    },
}
```

---

## Advanced Analytics

### Productivity Trends

```python
# Analyze productivity trends over time
trends = agent.analytics.productivity_trends(
    period="last_90_days",
    metrics=["focus_score", "tasks_completed", "habit_consistency"],
)

print("Productivity Trends (Last 90 Days):")
for metric, data in trends.items():
    print(f"\n{metric}:")
    print(f"  Current: {data['current']:.1f}")
    print(f"  Average: {data['average']:.1f}")
    print(f"  Trend: {data['trend']} ({data['change']:.1f}%)")
    print(f"  Best Day: {data['best_day']}")
    print(f"  Worst Day: {data['worst_day']}")
```

### Correlation Analysis

```python
# Find correlations between different metrics
correlations = agent.analytics.find_correlations(
    metrics=["focus_score", "sleep_hours", "exercise_minutes", "tasks_completed"],
    period="last_30_days",
)

print("Metric Correlations:")
for metric_pair, correlation in correlations.items():
    strength = "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.4 else "weak"
    direction = "positive" if correlation > 0 else "negative"
    print(f"  {metric_pair}: {correlation:.2f} ({strength} {direction})")
```

---

*Maximize your productivity potential through AI-driven automation that optimizes every aspect of your workday.*

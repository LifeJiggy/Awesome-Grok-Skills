"""
Productivity Agent
Personal and team productivity, time management, goal tracking,
habit formation, automation, and focus techniques.

Comprehensive implementation featuring:
- Task management with dependency graphs
- Time tracking and pomodoro technique
- Goal setting (SMART framework)
- Habit formation and streak tracking
- Calendar and schedule optimization
- Focus mode and deep work management
- Energy level monitoring
- Workflow automation
- Meeting management
- Decision journal
- Personal analytics and insights
- Team productivity dashboards
"""

from __future__ import annotations

import abc
import collections
import hashlib
import json
import logging
import math
import statistics
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Priority(Enum):
    """Task priority levels (1 = highest)."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    OPTIONAL = 5


class TaskStatus(Enum):
    """Task lifecycle states."""
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EnergyLevel(Enum):
    """Energy and focus levels."""
    PEAK = "peak"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEPLETED = "depleted"


class HabitFrequency(Enum):
    """How often a habit should be performed."""
    DAILY = "daily"
    WEEKDAYS = "weekdays"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class MeetingType(Enum):
    """Types of meetings."""
    STANDUP = "standup"
    ONE_ON_ONE = "one_on_one"
    SPRINT_PLANNING = "sprint_planning"
    RETROSPECTIVE = "retrospective"
    BRAINSTORM = "brainstorm"
    DECISION = "decision"
    STATUS_UPDATE = "status_update"
    WORKSHOP = "workshop"


class FocusMode(Enum):
    """Focus and attention modes."""
    DEEP_WORK = "deep_work"
    SHALLOW_WORK = "shallow_work"
    ADMIN = "admin"
    COMMUNICATION = "communication"
    LEARNING = "learning"
    CREATIVE = "creative"


class AutomationTrigger(Enum):
    """Triggers for workflow automation."""
    TIME_BASED = "time_based"
    EVENT_BASED = "event_based"
    CONDITION_BASED = "condition_based"
    MANUAL = "manual"


class DecisionType(Enum):
    """Types of decisions to journal."""
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    PERSONAL = "personal"
    FINANCIAL = "financial"


class ReviewPeriod(Enum):
    """Periods for productivity review."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """A trackable task with metadata."""
    task_id: str
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    created_at: datetime
    due_date: Optional[datetime]
    estimated_hours: float
    actual_hours: float
    tags: List[str]
    dependencies: List[str]
    subtasks: List[str]
    assignee: str
    project: str
    energy_required: EnergyLevel
    context: Dict[str, Any]
    completed_at: Optional[datetime] = None


@dataclass
class TimeEntry:
    """A time tracking entry."""
    entry_id: str
    task_id: Optional[str]
    description: str
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: float
    category: str
    focus_mode: FocusMode
    interruptions: int


@dataclass
class PomodoroSession:
    """A pomodoro focus session."""
    session_id: str
    task_id: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: int
    breaks_taken: int
    completed: bool
    interruptions: int
    focus_score: float


@dataclass
class Goal:
    """A SMART goal."""
    goal_id: str
    statement: str
    category: str
    specific: str
    measurable: str
    achievable: str
    relevant: str
    time_bound: str
    progress_pct: float
    milestones: List[Milestone]
    owner: str
    created_at: datetime
    target_date: datetime
    status: str


@dataclass
class Milestone:
    """A milestone within a goal."""
    milestone_id: str
    name: str
    target_date: datetime
    completed: bool
    completed_at: Optional[datetime]


@dataclass
class Habit:
    """A tracked habit."""
    habit_id: str
    name: str
    description: str
    frequency: HabitFrequency
    target_count: int
    current_streak: int
    longest_streak: int
    completions: List[datetime]
    created_at: datetime
    archived: bool = False


@dataclass
class CalendarBlock:
    """A time block on the calendar."""
    block_id: str
    title: str
    start_time: datetime
    end_time: datetime
    category: str
    is_recurring: bool
    recurrence_rule: Optional[str]
    focus_mode: FocusMode
    meeting_type: Optional[MeetingType]


@dataclass
class Meeting:
    """A scheduled meeting."""
    meeting_id: str
    title: str
    meeting_type: MeetingType
    attendees: List[str]
    start_time: datetime
    end_time: datetime
    agenda: List[str]
    action_items: List[str]
    notes: str
    outcome: str


@dataclass
class EnergySnapshot:
    """An energy level observation."""
    snapshot_id: str
    timestamp: datetime
    energy_level: EnergyLevel
    focus_score: float
    mood: str
    notes: str
    activities_before: List[str]


@dataclass
class Workflow:
    """An automated workflow."""
    workflow_id: str
    name: str
    description: str
    trigger: AutomationTrigger
    trigger_config: Dict[str, Any]
    steps: List[WorkflowStep]
    enabled: bool
    last_run: Optional[datetime]
    run_count: int


@dataclass
class WorkflowStep:
    """A step within an automated workflow."""
    step_id: str
    name: str
    action: str
    config: Dict[str, Any]
    order: int
    condition: Optional[str]


@dataclass
class Decision:
    """A journal entry for a decision."""
    decision_id: str
    title: str
    decision_type: DecisionType
    context: str
    options: List[str]
    chosen_option: str
    reasoning: str
    expected_outcome: str
    actual_outcome: Optional[str]
    confidence_at_time: float
    date_made: datetime
    date_reviewed: Optional[datetime]
    lesson_learned: Optional[str]


@dataclass
class ProductivitySnapshot:
    """A point-in-time productivity measurement."""
    snapshot_id: str
    timestamp: datetime
    tasks_completed: int
    focus_hours: float
    meeting_hours: float
    productivity_score: float
    energy_average: float
    habits_completed: int
    goals_progress: float


@dataclass
class ProductivityConfig:
    """Configuration for the productivity agent."""
    pomodoro_duration: int = 25
    short_break_duration: int = 5
    long_break_duration: int = 15
    pomodoros_before_long_break: int = 4
    daily_focus_target_hours: float = 4.0
    meeting_budget_hours_per_day: float = 2.0
    habit_reminder_enabled: bool = True
    energy_tracking_interval_minutes: int = 60
    review_day_of_week: str = "friday"
    deep_work_hours: Tuple[int, int] = (9, 12)


# ---------------------------------------------------------------------------
# Task Manager
# ---------------------------------------------------------------------------

class TaskManager:
    """Manages task creation, tracking, and organization."""

    VALID_TRANSITIONS: Dict[TaskStatus, Set[TaskStatus]] = {
        TaskStatus.BACKLOG: {TaskStatus.TODO},
        TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
        TaskStatus.IN_PROGRESS: {TaskStatus.BLOCKED, TaskStatus.REVIEW, TaskStatus.COMPLETED, TaskStatus.CANCELLED},
        TaskStatus.BLOCKED: {TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED},
        TaskStatus.REVIEW: {TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED},
        TaskStatus.COMPLETED: set(),
        TaskStatus.CANCELLED: set(),
    }

    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}
        self._dependency_graph: Dict[str, Set[str]] = {}
        self._tags_index: Dict[str, Set[str]] = {}

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[datetime] = None,
        estimated_hours: float = 1.0,
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
        assignee: str = "",
        project: str = "",
        energy_required: EnergyLevel = EnergyLevel.MEDIUM,
    ) -> Task:
        if not title:
            raise ValueError("task title must not be empty")
        if due_date and due_date < datetime.utcnow():
            logger.warning("due date is in the past: %s", due_date)
        task = Task(
            task_id=str(uuid.uuid4())[:12],
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
            created_at=datetime.utcnow(),
            due_date=due_date,
            estimated_hours=estimated_hours,
            actual_hours=0.0,
            tags=tags or [],
            dependencies=dependencies or [],
            subtasks=[],
            assignee=assignee,
            project=project,
            energy_required=energy_required,
            context={},
        )
        self.tasks[task.task_id] = task
        for dep_id in task.dependencies:
            self._dependency_graph.setdefault(dep_id, set()).add(task.task_id)
        for tag in task.tags:
            self._tags_index.setdefault(tag, set()).add(task.task_id)
        logger.info("Task created: %s [%s]", title, task.task_id)
        return task

    def update_task(self, task_id: str, **updates: Any) -> Task:
        task = self._get_task(task_id)
        for key, value in updates.items():
            if hasattr(task, key) and key not in ("task_id", "created_at"):
                setattr(task, key, value)
        return task

    def transition(self, task_id: str, new_status: TaskStatus) -> Task:
        task = self._get_task(task_id)
        allowed = self.VALID_TRANSITIONS.get(task.status, set())
        if new_status not in allowed:
            raise ValueError(
                f"cannot transition from {task.status.value} to {new_status.value}"
            )
        task.status = new_status
        if new_status == TaskStatus.COMPLETED:
            task.completed_at = datetime.utcnow()
        return task

    def complete_task(self, task_id: str, hours_logged: float = 0.0) -> Task:
        task = self._get_task(task_id)
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.actual_hours = hours_logged
        return task

    def blocked_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]

    def overdue_tasks(self) -> List[Task]:
        now = datetime.utcnow()
        return [
            t for t in self.tasks.values()
            if t.due_date and t.due_date < now and t.status not in (TaskStatus.COMPLETED, TaskStatus.CANCELLED)
        ]

    def tasks_by_priority(self) -> List[Task]:
        return sorted(
            self.tasks.values(),
            key=lambda t: (t.priority.value, t.due_date or datetime.max),
        )

    def tasks_by_project(self, project: str) -> List[Task]:
        return [t for t in self.tasks.values() if t.project == project]

    def tasks_by_tag(self, tag: str) -> List[Task]:
        task_ids = self._tags_index.get(tag, set())
        return [self.tasks[tid] for tid in task_ids if tid in self.tasks]

    def dependency_chain(self, task_id: str) -> List[str]:
        chain: List[str] = []
        visited: Set[str] = set()
        self._dfs_dependencies(task_id, chain, visited)
        return chain

    def _dfs_dependencies(self, task_id: str, chain: List[str], visited: Set[str]) -> None:
        if task_id in visited:
            return
        visited.add(task_id)
        task = self.tasks.get(task_id)
        if task:
            for dep_id in task.dependencies:
                self._dfs_dependencies(dep_id, chain, visited)
            chain.append(task_id)

    def task_statistics(self) -> Dict[str, Any]:
        all_tasks = list(self.tasks.values())
        completed = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
        total_est = sum(t.estimated_hours for t in all_tasks)
        total_actual = sum(t.actual_hours for t in completed)
        return {
            "total": len(all_tasks),
            "completed": len(completed),
            "in_progress": sum(1 for t in all_tasks if t.status == TaskStatus.IN_PROGRESS),
            "blocked": sum(1 for t in all_tasks if t.status == TaskStatus.BLOCKED),
            "overdue": len(self.overdue_tasks()),
            "total_estimated_hours": total_est,
            "total_actual_hours": total_actual,
            "estimation_accuracy": round(total_actual / total_est * 100, 1) if total_est else 0,
            "by_priority": {
                p.value: sum(1 for t in all_tasks if t.priority == p)
                for p in Priority
            },
        }

    def _get_task(self, task_id: str) -> Task:
        if task_id not in self.tasks:
            raise ValueError(f"task {task_id} not found")
        return self.tasks[task_id]


# ---------------------------------------------------------------------------
# Time Tracker
# ---------------------------------------------------------------------------

class TimeTracker:
    """Tracks time spent on tasks and activities."""

    def __init__(self) -> None:
        self.entries: List[TimeEntry] = []
        self._active_entry: Optional[TimeEntry] = None

    def start_tracking(
        self,
        task_id: Optional[str] = None,
        description: str = "",
        category: str = "general",
        focus_mode: FocusMode = FocusMode.SHALLOW_WORK,
    ) -> TimeEntry:
        if self._active_entry:
            raise RuntimeError("already tracking time — stop first")
        entry = TimeEntry(
            entry_id=str(uuid.uuid4())[:12],
            task_id=task_id,
            description=description,
            start_time=datetime.utcnow(),
            end_time=None,
            duration_minutes=0.0,
            category=category,
            focus_mode=focus_mode,
            interruptions=0,
        )
        self._active_entry = entry
        return entry

    def stop_tracking(self) -> TimeEntry:
        if not self._active_entry:
            raise RuntimeError("no active time entry")
        entry = self._active_entry
        entry.end_time = datetime.utcnow()
        entry.duration_minutes = (entry.end_time - entry.start_time).total_seconds() / 60
        self.entries.append(entry)
        self._active_entry = None
        return entry

    def record_interruption(self) -> None:
        if self._active_entry:
            self._active_entry.interruptions += 1

    def manual_entry(
        self,
        start: datetime,
        end: datetime,
        task_id: Optional[str] = None,
        description: str = "",
        category: str = "general",
        focus_mode: FocusMode = FocusMode.SHALLOW_WORK,
    ) -> TimeEntry:
        entry = TimeEntry(
            entry_id=str(uuid.uuid4())[:12],
            task_id=task_id,
            description=description,
            start_time=start,
            end_time=end,
            duration_minutes=(end - start).total_seconds() / 60,
            category=category,
            focus_mode=focus_mode,
            interruptions=0,
        )
        self.entries.append(entry)
        return entry

    def daily_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        target = date or datetime.utcnow()
        day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_entries = [
            e for e in self.entries
            if e.start_time >= day_start and e.start_time < day_end
        ]
        if not day_entries:
            return {"date": day_start.date().isoformat(), "total_minutes": 0}
        total = sum(e.duration_minutes for e in day_entries)
        by_category: Dict[str, float] = {}
        by_focus: Dict[str, float] = {}
        for e in day_entries:
            by_category[e.category] = by_category.get(e.category, 0) + e.duration_minutes
            by_focus[e.focus_mode.value] = by_focus.get(e.focus_mode.value, 0) + e.duration_minutes
        return {
            "date": day_start.date().isoformat(),
            "total_minutes": round(total, 1),
            "total_hours": round(total / 60, 2),
            "entry_count": len(day_entries),
            "by_category": by_category,
            "by_focus_mode": by_focus,
            "interruptions": sum(e.interruptions for e in day_entries),
        }

    def weekly_summary(self) -> Dict[str, Any]:
        today = datetime.utcnow()
        week_start = today - timedelta(days=today.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_entries = [e for e in self.entries if e.start_time >= week_start]
        daily: Dict[str, float] = {}
        for e in week_entries:
            day_key = e.start_time.date().isoformat()
            daily[day_key] = daily.get(day_key, 0) + e.duration_minutes
        return {
            "week_start": week_start.date().isoformat(),
            "total_hours": round(sum(daily.values()) / 60, 2),
            "daily_breakdown": daily,
            "avg_daily_hours": round(sum(daily.values()) / 60 / max(len(daily), 1), 2),
        }

    def focus_score(self, hours: float = 8.0) -> float:
        today = datetime.utcnow()
        day_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        day_entries = [
            e for e in self.entries
            if e.start_time >= day_start
        ]
        if not day_entries:
            return 0.0
        deep_work = sum(
            e.duration_minutes for e in day_entries
            if e.focus_mode == FocusMode.DEEP_WORK
        )
        total = sum(e.duration_minutes for e in day_entries)
        interruptions = sum(e.interruptions for e in day_entries)
        score = (deep_work / max(total, 1)) * 100
        score -= min(interruptions * 2, 20)
        return round(max(min(score, 100), 0), 1)


# ---------------------------------------------------------------------------
# Pomodoro Timer
# ---------------------------------------------------------------------------

class PomodoroTimer:
    """Manages pomodoro focus sessions."""

    def __init__(self, config: Optional[ProductivityConfig] = None) -> None:
        self.config = config or ProductivityConfig()
        self.sessions: List[PomodoroSession] = []
        self._active_session: Optional[PomodoroSession] = None
        self._today_count: int = 0

    def start_session(self, task_id: Optional[str] = None) -> PomodoroSession:
        if self._active_session:
            raise RuntimeError("pomodoro session already active")
        session = PomodoroSession(
            session_id=str(uuid.uuid4())[:12],
            task_id=task_id,
            start_time=datetime.utcnow(),
            end_time=None,
            duration_minutes=self.config.pomodoro_duration,
            breaks_taken=0,
            completed=False,
            interruptions=0,
            focus_score=0.0,
        )
        self._active_session = session
        logger.info("Pomodoro started: %s", session.session_id)
        return session

    def complete_session(self) -> PomodoroSession:
        if not self._active_session:
            raise RuntimeError("no active pomodoro session")
        session = self._active_session
        session.end_time = datetime.utcnow()
        session.completed = True
        session.focus_score = self._calculate_focus_score(session)
        self.sessions.append(session)
        self._active_session = None
        self._today_count += 1
        logger.info("Pomodoro completed (#%d today)", self._today_count)
        return session

    def interrupt_session(self) -> None:
        if self._active_session:
            self._active_session.interruptions += 1

    def take_break(self) -> Dict[str, Any]:
        is_long = self._today_count > 0 and self._today_count % self.config.pomodoros_before_long_break == 0
        duration = self.config.long_break_duration if is_long else self.config.short_break_duration
        if self._active_session:
            self._active_session.breaks_taken += 1
        return {
            "break_type": "long" if is_long else "short",
            "duration_minutes": duration,
            "pomodoros_completed": self._today_count,
        }

    def daily_stats(self) -> Dict[str, Any]:
        today = datetime.utcnow().date()
        today_sessions = [
            s for s in self.sessions
            if s.start_time.date() == today
        ]
        if not today_sessions:
            return {"pomodoros": 0, "focus_minutes": 0}
        completed = [s for s in today_sessions if s.completed]
        focus_minutes = sum(s.duration_minutes for s in completed)
        avg_focus = (
            statistics.mean(s.focus_score for s in completed)
            if completed else 0
        )
        return {
            "pomodoros": len(completed),
            "focus_minutes": focus_minutes,
            "avg_focus_score": round(avg_focus, 1),
            "total_interruptions": sum(s.interruptions for s in today_sessions),
            "target_remaining": max(0, int(self.config.daily_focus_target_hours * 60 / self.config.pomodoro_duration) - len(completed)),
        }

    def _calculate_focus_score(self, session: PomodoroSession) -> float:
        base = 100.0
        interruption_penalty = session.interruptions * 10
        break_bonus = min(session.breaks_taken * 5, 15)
        return round(max(min(base - interruption_penalty + break_bonus, 100), 0), 1)


# ---------------------------------------------------------------------------
# Goal Tracker
# ---------------------------------------------------------------------------

class GoalTracker:
    """Sets and tracks SMART goals."""

    def __init__(self) -> None:
        self.goals: Dict[str, Goal] = {}

    def create_goal(
        self,
        statement: str,
        category: str,
        specific: str,
        measurable: str,
        achievable: str,
        relevant: str,
        time_bound: str,
        owner: str,
        target_date: datetime,
        milestones: Optional[List[Dict[str, Any]]] = None,
    ) -> Goal:
        ms: List[Milestone] = []
        for m in (milestones or []):
            ms.append(Milestone(
                milestone_id=str(uuid.uuid4())[:12],
                name=m["name"],
                target_date=m.get("target_date", target_date),
                completed=False,
                completed_at=None,
            ))
        goal = Goal(
            goal_id=str(uuid.uuid4())[:12],
            statement=statement,
            category=category,
            specific=specific,
            measurable=measurable,
            achievable=achievable,
            relevant=relevant,
            time_bound=time_bound,
            progress_pct=0.0,
            milestones=ms,
            owner=owner,
            created_at=datetime.utcnow(),
            target_date=target_date,
            status="active",
        )
        self.goals[goal.goal_id] = goal
        logger.info("Goal created: %s", statement[:60])
        return goal

    def update_progress(self, goal_id: str, progress_pct: float) -> Goal:
        goal = self._get_goal(goal_id)
        goal.progress_pct = min(max(progress_pct, 0), 100)
        if goal.progress_pct >= 100:
            goal.status = "achieved"
        return goal

    def complete_milestone(self, goal_id: str, milestone_id: str) -> Goal:
        goal = self._get_goal(goal_id)
        for ms in goal.milestones:
            if ms.milestone_id == milestone_id:
                ms.completed = True
                ms.completed_at = datetime.utcnow()
                break
        completed = sum(1 for m in goal.milestones if m.completed)
        total = len(goal.milestones)
        goal.progress_pct = (completed / total * 100) if total else 0
        return goal

    def goals_status(self) -> Dict[str, Any]:
        goals = list(self.goals.values())
        return {
            "total": len(goals),
            "active": sum(1 for g in goals if g.status == "active"),
            "achieved": sum(1 for g in goals if g.status == "achieved"),
            "avg_progress": round(
                statistics.mean(g.progress_pct for g in goals) if goals else 0, 1
            ),
            "by_category": {
                cat: sum(1 for g in goals if g.category == cat)
                for cat in set(g.category for g in goals)
            },
        }

    def _get_goal(self, goal_id: str) -> Goal:
        if goal_id not in self.goals:
            raise ValueError(f"goal {goal_id} not found")
        return self.goals[goal_id]


# ---------------------------------------------------------------------------
# Habit Tracker
# ---------------------------------------------------------------------------

class HabitTracker:
    """Tracks habits and streaks."""

    def __init__(self) -> None:
        self.habits: Dict[str, Habit] = {}

    def create_habit(
        self,
        name: str,
        description: str,
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_count: int = 1,
    ) -> Habit:
        habit = Habit(
            habit_id=str(uuid.uuid4())[:12],
            name=name,
            description=description,
            frequency=frequency,
            target_count=target_count,
            current_streak=0,
            longest_streak=0,
            completions=[],
            created_at=datetime.utcnow(),
        )
        self.habits[habit.habit_id] = habit
        logger.info("Habit created: %s", name)
        return habit

    def complete_habit(self, habit_id: str) -> Habit:
        habit = self._get_habit(habit_id)
        now = datetime.utcnow()
        habit.completions.append(now)
        if habit.completions:
            last = habit.completions[-2] if len(habit.completions) > 1 else None
            if last:
                days_diff = (now.date() - last.date()).days
                if days_diff <= 1:
                    habit.current_streak += 1
                else:
                    habit.current_streak = 1
            else:
                habit.current_streak = 1
        habit.longest_streak = max(habit.longest_streak, habit.current_streak)
        return habit

    def check_streak(self, habit_id: str) -> Dict[str, Any]:
        habit = self._get_habit(habit_id)
        today = datetime.utcnow().date()
        today_completed = any(
            c.date() == today for c in habit.completions
        )
        return {
            "habit": habit.name,
            "current_streak": habit.current_streak,
            "longest_streak": habit.longest_streak,
            "completed_today": today_completed,
            "frequency": habit.frequency.value,
        }

    def habits_dashboard(self) -> Dict[str, Any]:
        active = [h for h in self.habits.values() if not h.archived]
        today = datetime.utcnow().date()
        completed_today = sum(
            1 for h in active
            if any(c.date() == today for c in h.completions)
        )
        return {
            "total_habits": len(active),
            "completed_today": completed_today,
            "completion_rate": round(
                completed_today / len(active) * 100, 1
            ) if active else 0,
            "avg_streak": round(
                statistics.mean(h.current_streak for h in active) if active else 0, 1
            ),
            "habits": [
                {
                    "name": h.name,
                    "streak": h.current_streak,
                    "frequency": h.frequency.value,
                }
                for h in active
            ],
        }

    def _get_habit(self, habit_id: str) -> Habit:
        if habit_id not in self.habits:
            raise ValueError(f"habit {habit_id} not found")
        return self.habits[habit_id]


# ---------------------------------------------------------------------------
# Calendar Optimizer
# ---------------------------------------------------------------------------

class CalendarOptimizer:
    """Manages time blocks and optimizes schedules."""

    def __init__(self, config: Optional[ProductivityConfig] = None) -> None:
        self.config = config or ProductivityConfig()
        self.blocks: Dict[str, CalendarBlock] = {}

    def add_block(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        category: str = "work",
        focus_mode: FocusMode = FocusMode.SHALLOW_WORK,
        meeting_type: Optional[MeetingType] = None,
    ) -> CalendarBlock:
        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")
        block = CalendarBlock(
            block_id=str(uuid.uuid4())[:12],
            title=title,
            start_time=start_time,
            end_time=end_time,
            category=category,
            is_recurring=False,
            recurrence_rule=None,
            focus_mode=focus_mode,
            meeting_type=meeting_type,
        )
        self.blocks[block.block_id] = block
        return block

    def find_free_slots(
        self,
        day: datetime,
        min_duration_minutes: int = 30,
    ) -> List[Tuple[datetime, datetime]]:
        day_start = day.replace(hour=8, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=18, minute=0, second=0, microsecond=0)
        day_blocks = sorted(
            [b for b in self.blocks.values()
             if b.start_time.date() == day.date()],
            key=lambda b: b.start_time,
        )
        free: List[Tuple[datetime, datetime]] = []
        current = day_start
        for block in day_blocks:
            if block.start_time > current:
                diff = (block.start_time - current).total_seconds() / 60
                if diff >= min_duration_minutes:
                    free.append((current, block.start_time))
            current = max(current, block.end_time)
        if current < day_end:
            diff = (day_end - current).total_seconds() / 60
            if diff >= min_duration_minutes:
                free.append((current, day_end))
        return free

    def meeting_load(self, week_start: datetime) -> Dict[str, Any]:
        week_end = week_start + timedelta(days=7)
        week_blocks = [
            b for b in self.blocks.values()
            if b.meeting_type and b.start_time >= week_start and b.start_time < week_end
        ]
        total_minutes = sum(
            (b.end_time - b.start_time).total_seconds() / 60
            for b in week_blocks
        )
        return {
            "total_meetings": len(week_blocks),
            "total_hours": round(total_minutes / 60, 1),
            "daily_avg_hours": round(total_minutes / 60 / 5, 1),
            "by_type": {
                mt.value: sum(
                    1 for b in week_blocks if b.meeting_type == mt
                )
                for mt in MeetingType
            },
        }

    def protect_focus_time(self, day: datetime) -> List[CalendarBlock]:
        free = self.find_free_slots(day, min_duration_minutes=60)
        blocks: List[CalendarBlock] = []
        for start, end in free[:2]:
            block = self.add_block(
                title="Deep Focus Time",
                start_time=start,
                end_time=end,
                category="focus",
                focus_mode=FocusMode.DEEP_WORK,
            )
            blocks.append(block)
        return blocks


# ---------------------------------------------------------------------------
# Meeting Manager
# ---------------------------------------------------------------------------

class MeetingManager:
    """Manages meetings, agendas, and action items."""

    def __init__(self) -> None:
        self.meetings: Dict[str, Meeting] = {}

    def schedule_meeting(
        self,
        title: str,
        meeting_type: MeetingType,
        attendees: List[str],
        start_time: datetime,
        end_time: datetime,
        agenda: Optional[List[str]] = None,
    ) -> Meeting:
        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")
        meeting = Meeting(
            meeting_id=str(uuid.uuid4())[:12],
            title=title,
            meeting_type=meeting_type,
            attendees=attendees,
            start_time=start_time,
            end_time=end_time,
            agenda=agenda or [],
            action_items=[],
            notes="",
            outcome="",
        )
        self.meetings[meeting.meeting_id] = meeting
        logger.info("Meeting scheduled: %s", title)
        return meeting

    def add_action_item(self, meeting_id: str, action: str) -> Meeting:
        meeting = self._get_meeting(meeting_id)
        meeting.action_items.append(action)
        return meeting

    def complete_meeting(
        self,
        meeting_id: str,
        notes: str,
        outcome: str,
    ) -> Meeting:
        meeting = self._get_meeting(meeting_id)
        meeting.notes = notes
        meeting.outcome = outcome
        return meeting

    def meeting_efficiency(self, meeting_id: str) -> Dict[str, Any]:
        meeting = self._get_meeting(meeting_id)
        duration = (meeting.end_time - meeting.start_time).total_seconds() / 60
        agenda_items = len(meeting.agenda)
        actions = len(meeting.action_items)
        return {
            "title": meeting.title,
            "type": meeting.meeting_type.value,
            "duration_minutes": round(duration, 1),
            "attendees": len(meeting.attendees),
            "agenda_items": agenda_items,
            "action_items": actions,
            "has_outcome": bool(meeting.outcome),
            "efficiency_score": round(
                (actions / max(agenda_items, 1)) * 100, 1
            ) if agenda_items else 0,
        }

    def recurring_meeting_analysis(self) -> Dict[str, Any]:
        by_type: Dict[str, List[Meeting]] = {}
        for m in self.meetings.values():
            by_type.setdefault(m.meeting_type.value, []).append(m)
        analysis: List[Dict[str, Any]] = []
        for mt, meetings in by_type.items():
            avg_duration = statistics.mean(
                (m.end_time - m.start_time).total_seconds() / 60
                for m in meetings
            )
            total_actions = sum(len(m.action_items) for m in meetings)
            analysis.append({
                "type": mt,
                "count": len(meetings),
                "avg_duration_minutes": round(avg_duration, 1),
                "total_actions": total_actions,
                "actions_per_meeting": round(total_actions / len(meetings), 1) if meetings else 0,
            })
        return {"meeting_types": analysis}

    def _get_meeting(self, meeting_id: str) -> Meeting:
        if meeting_id not in self.meetings:
            raise ValueError(f"meeting {meeting_id} not found")
        return self.meetings[meeting_id]


# ---------------------------------------------------------------------------
# Energy Tracker
# ---------------------------------------------------------------------------

class EnergyTracker:
    """Tracks energy levels and patterns."""

    def __init__(self, config: Optional[ProductivityConfig] = None) -> None:
        self.config = config or ProductivityConfig()
        self.snapshots: List[EnergySnapshot] = []

    def record_snapshot(
        self,
        energy_level: EnergyLevel,
        focus_score: float,
        mood: str = "",
        notes: str = "",
        activities_before: Optional[List[str]] = None,
    ) -> EnergySnapshot:
        snapshot = EnergySnapshot(
            snapshot_id=str(uuid.uuid4())[:12],
            timestamp=datetime.utcnow(),
            energy_level=energy_level,
            focus_score=focus_score,
            mood=mood,
            notes=notes,
            activities_before=activities_before or [],
        )
        self.snapshots.append(snapshot)
        return snapshot

    def daily_pattern(self) -> Dict[str, Any]:
        today = datetime.utcnow().date()
        today_snapshots = [
            s for s in self.snapshots
            if s.timestamp.date() == today
        ]
        if not today_snapshots:
            return {"pattern": "no data"}
        hourly: Dict[int, List[float]] = {}
        for s in today_snapshots:
            hour = s.timestamp.hour
            hourly.setdefault(hour, []).append(s.focus_score)
        pattern: List[Dict[str, Any]] = []
        for hour in sorted(hourly.keys()):
            scores = hourly[hour]
            pattern.append({
                "hour": hour,
                "avg_focus": round(statistics.mean(scores), 1),
                "samples": len(scores),
            })
        return {"pattern": pattern, "peak_hour": max(pattern, key=lambda x: x["avg_focus"])["hour"] if pattern else None}

    def energy_recommendations(self) -> List[str]:
        if not self.snapshots:
            return ["Start tracking your energy levels to get personalized recommendations."]
        recent = self.snapshots[-10:]
        low_hours: List[int] = []
        high_hours: List[int] = []
        for s in recent:
            if s.energy_level in (EnergyLevel.LOW, EnergyLevel.DEEPDED):
                low_hours.append(s.timestamp.hour)
            elif s.energy_level in (EnergyLevel.PEAK, EnergyLevel.HIGH):
                high_hours.append(s.timestamp.hour)
        recs: List[str] = []
        if high_hours:
            peak = max(set(high_hours), key=high_hours.count)
            recs.append(f"Schedule deep work around {peak}:00 when your energy peaks.")
        if low_hours:
            dip = max(set(low_hours), key=low_hours.count)
            recs.append(f"Avoid meetings around {dip}:00 during your energy dip.")
        avg_focus = statistics.mean(s.focus_score for s in recent)
        if avg_focus < 50:
            recs.append("Consider more frequent breaks to improve focus scores.")
        return recs

    def weekly_energy_report(self) -> Dict[str, Any]:
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_snapshots = [s for s in self.snapshots if s.timestamp >= week_ago]
        if not week_snapshots:
            return {"report": "no data for this week"}
        by_level = {level.value: 0 for level in EnergyLevel}
        for s in week_snapshots:
            by_level[s.energy_level.value] += 1
        return {
            "total_snapshots": len(week_snapshots),
            "energy_distribution": by_level,
            "avg_focus": round(statistics.mean(s.focus_score for s in week_snapshots), 1),
            "moods": list(set(s.mood for s in week_snapshots if s.mood)),
        }


# ---------------------------------------------------------------------------
# Workflow Automation
# ---------------------------------------------------------------------------

class WorkflowAutomation:
    """Manages automated workflows."""

    def __init__(self) -> None:
        self.workflows: Dict[str, Workflow] = {}
        self._execution_log: List[Dict[str, Any]] = []

    def create_workflow(
        self,
        name: str,
        description: str,
        trigger: AutomationTrigger,
        trigger_config: Dict[str, Any],
        steps: List[Dict[str, Any]],
    ) -> Workflow:
        wf_steps: List[WorkflowStep] = []
        for i, step in enumerate(steps):
            ws = WorkflowStep(
                step_id=str(uuid.uuid4())[:12],
                name=step.get("name", f"Step {i + 1}"),
                action=step.get("action", ""),
                config=step.get("config", {}),
                order=i,
                condition=step.get("condition"),
            )
            wf_steps.append(ws)
        workflow = Workflow(
            workflow_id=str(uuid.uuid4())[:12],
            name=name,
            description=description,
            trigger=trigger,
            trigger_config=trigger_config,
            steps=wf_steps,
            enabled=True,
            last_run=None,
            run_count=0,
        )
        self.workflows[workflow.workflow_id] = workflow
        logger.info("Workflow created: %s", name)
        return workflow

    def execute_workflow(self, workflow_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        wf = self._get_workflow(workflow_id)
        if not wf.enabled:
            raise RuntimeError(f"workflow {wf.name} is disabled")
        results: List[Dict[str, Any]] = []
        for step in sorted(wf.steps, key=lambda s: s.order):
            if step.condition:
                if not self._evaluate_condition(step.condition, context):
                    results.append({"step": step.name, "skipped": True})
                    continue
            result = {"step": step.name, "action": step.action, "executed": True}
            results.append(result)
        wf.last_run = datetime.utcnow()
        wf.run_count += 1
        self._execution_log.append({
            "workflow_id": workflow_id,
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
        })
        return {"workflow": wf.name, "steps_executed": len(results), "results": results}

    def toggle_workflow(self, workflow_id: str) -> Workflow:
        wf = self._get_workflow(workflow_id)
        wf.enabled = not wf.enabled
        return wf

    def workflow_stats(self) -> Dict[str, Any]:
        workflows = list(self.workflows.values())
        return {
            "total": len(workflows),
            "enabled": sum(1 for w in workflows if w.enabled),
            "total_runs": sum(w.run_count for w in workflows),
            "most_used": max(workflows, key=lambda w: w.run_count).name if workflows else None,
        }

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        return True

    def _get_workflow(self, workflow_id: str) -> Workflow:
        if workflow_id not in self.workflows:
            raise ValueError(f"workflow {workflow_id} not found")
        return self.workflows[workflow_id]


# ---------------------------------------------------------------------------
# Decision Journal
# ---------------------------------------------------------------------------

class DecisionJournal:
    """Logs and reviews decisions."""

    def __init__(self) -> None:
        self.decisions: Dict[str, Decision] = {}

    def log_decision(
        self,
        title: str,
        decision_type: DecisionType,
        context: str,
        options: List[str],
        chosen_option: str,
        reasoning: str,
        expected_outcome: str,
        confidence: float,
    ) -> Decision:
        decision = Decision(
            decision_id=str(uuid.uuid4())[:12],
            title=title,
            decision_type=decision_type,
            context=context,
            options=options,
            chosen_option=chosen_option,
            reasoning=reasoning,
            expected_outcome=expected_outcome,
            actual_outcome=None,
            confidence_at_time=confidence,
            date_made=datetime.utcnow(),
            date_reviewed=None,
            lesson_learned=None,
        )
        self.decisions[decision.decision_id] = decision
        logger.info("Decision logged: %s", title)
        return decision

    def review_decision(
        self,
        decision_id: str,
        actual_outcome: str,
        lesson_learned: str,
    ) -> Decision:
        decision = self._get_decision(decision_id)
        decision.actual_outcome = actual_outcome
        decision.lesson_learned = lesson_learned
        decision.date_reviewed = datetime.utcnow()
        return decision

    def accuracy_report(self) -> Dict[str, Any]:
        reviewed = [d for d in self.decisions.values() if d.date_reviewed]
        if not reviewed:
            return {"reviewed": 0, "accuracy": 0}
        correct = sum(
            1 for d in reviewed
            if d.actual_outcome and d.lesson_learned
        )
        return {
            "total_decisions": len(self.decisions),
            "reviewed": len(reviewed),
            "accuracy": round(correct / len(reviewed) * 100, 1) if reviewed else 0,
            "avg_confidence": round(
                statistics.mean(d.confidence_at_time for d in reviewed), 2
            ) if reviewed else 0,
        }

    def _get_decision(self, decision_id: str) -> Decision:
        if decision_id not in self.decisions:
            raise ValueError(f"decision {decision_id} not found")
        return self.decisions[decision_id]


# ---------------------------------------------------------------------------
# Productivity Analytics
# ---------------------------------------------------------------------------

class ProductivityAnalytics:
    """Generates insights from productivity data."""

    def __init__(
        self,
        task_manager: TaskManager,
        time_tracker: TimeTracker,
        habit_tracker: HabitTracker,
        goal_tracker: GoalTracker,
    ) -> None:
        self.tasks = task_manager
        self.time = time_tracker
        self.habits = habit_tracker
        self.goals = goal_tracker

    def productivity_score(self) -> float:
        task_stats = self.tasks.task_statistics()
        completion_rate = task_stats["completed"] / max(task_stats["total"], 1)
        time_data = self.time.daily_summary()
        focus_hours = time_data.get("total_hours", 0)
        habit_data = self.habits.habits_dashboard()
        habit_rate = habit_data.get("completion_rate", 0) / 100
        score = (
            completion_rate * 40
            + min(focus_hours / 8, 1) * 30
            + habit_rate * 30
        )
        return round(min(score, 100), 1)

    def weekly_insights(self) -> Dict[str, Any]:
        task_stats = self.tasks.task_statistics()
        time_summary = self.time.weekly_summary()
        habit_dash = self.habits.habits_dashboard()
        goal_status = self.goals.goals_status()
        return {
            "tasks": task_stats,
            "time": time_summary,
            "habits": habit_dash,
            "goals": goal_status,
            "productivity_score": self.productivity_score(),
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        recs: List[str] = []
        task_stats = self.tasks.task_statistics()
        if task_stats["blocked"] > 0:
            recs.append(f"You have {task_stats['blocked']} blocked tasks — prioritize unblocking them.")
        if task_stats["overdue"] > 0:
            recs.append(f"{task_stats['overdue']} tasks are overdue — reprioritize or extend deadlines.")
        if task_stats.get("estimation_accuracy", 0) < 80:
            recs.append("Estimation accuracy is low — consider breaking tasks into smaller pieces.")
        time_data = self.time.daily_summary()
        if time_data.get("total_hours", 0) < 4:
            recs.append("Focus time is below target — protect deep work blocks.")
        return recs

    def generate_snapshot(self) -> ProductivitySnapshot:
        task_stats = self.tasks.task_statistics()
        time_data = self.time.daily_summary()
        habit_data = self.habits.habits_dashboard()
        goal_status = self.goals.goals_status()
        return ProductivitySnapshot(
            snapshot_id=str(uuid.uuid4())[:12],
            timestamp=datetime.utcnow(),
            tasks_completed=task_stats["completed"],
            focus_hours=time_data.get("total_hours", 0),
            meeting_hours=0.0,
            productivity_score=self.productivity_score(),
            energy_average=0.0,
            habits_completed=habit_data.get("completed_today", 0),
            goals_progress=goal_status.get("avg_progress", 0),
        )


# ---------------------------------------------------------------------------
# Productivity Agent (Orchestrator)
# ---------------------------------------------------------------------------

class ProductivityAgent:
    """Orchestrates all productivity sub-components."""

    def __init__(self, config: Optional[ProductivityConfig] = None) -> None:
        self.config = config or ProductivityConfig()
        self.tasks = TaskManager()
        self.time = TimeTracker()
        self.pomodoro = PomodoroTimer(self.config)
        self.goals = GoalTracker()
        self.habits = HabitTracker()
        self.calendar = CalendarOptimizer(self.config)
        self.meetings = MeetingManager()
        self.energy = EnergyTracker(self.config)
        self.workflows = WorkflowAutomation()
        self.decisions = DecisionJournal()
        self.analytics = ProductivityAnalytics(
            self.tasks, self.time, self.habits, self.goals
        )
        logger.info("ProductivityAgent initialized")

    def full_status(self) -> Dict[str, Any]:
        return {
            "tasks": self.tasks.task_statistics(),
            "time_today": self.time.daily_summary(),
            "pomodoros_today": self.pomodoro.daily_stats(),
            "habits": self.habits.habits_dashboard(),
            "goals": self.goals.goals_status(),
            "productivity_score": self.analytics.productivity_score(),
            "workflows": self.workflows.workflow_stats(),
        }

    def run(self) -> Dict[str, Any]:
        logger.info("ProductivityAgent run starting")
        status = self.full_status()
        logger.info("ProductivityAgent run complete")
        return status


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    agent = ProductivityAgent()
    result = agent.run()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

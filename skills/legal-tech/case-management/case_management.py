"""
Case Management Module
Legal case management and workflow automation
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MatterStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ON_HOLD = "on_hold"
    ARCHIVED = "archived"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class DeadlineType(Enum):
    COURT_FILING = "court_filing"
    STATUTE = "statute"
    INTERNAL = "internal"
    CLIENT = "client"

@dataclass
class Matter:
    matter_id: str = ""
    client: str = ""
    matter_type: str = ""
    description: str = ""
    responsible_attorney: str = ""
    status: MatterStatus = MatterStatus.ACTIVE
    opened_date: str = ""

@dataclass
class Deadline:
    description: str = ""
    due_date: str = ""
    deadline_type: DeadlineType = DeadlineType.COURT_FILING
    responsible_attorney: str = ""
    alert_days_before: int = 14
    id: str = field(default_factory=lambda: f"DL-{str(uuid.uuid4())[:8]}")

@dataclass
class LegalTask:
    title: str = ""
    assignee: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: str = ""
    estimated_hours: float = 0.0
    id: str = field(default_factory=lambda: f"TASK-{str(uuid.uuid4())[:8]}")

@dataclass
class TimeEntry:
    attorney: str = ""
    date: str = ""
    hours: float = 0.0
    description: str = ""
    activity_type: str = ""
    billable: bool = True
    id: str = field(default_factory=lambda: f"TE-{str(uuid.uuid4())[:8]}")

class CaseManager:
    def __init__(self) -> None:
        self._matters: Dict[str, Matter] = {}

    def create_matter(self, matter: Matter) -> str:
        self._matters[matter.matter_id] = matter
        return matter.matter_id

    def get_matter(self, matter_id: str) -> Optional[Matter]:
        return self._matters.get(matter_id)

class DeadlineTracker:
    def __init__(self, matter_id: str = "") -> None:
        self.matter_id = matter_id
        self._deadlines: List[Deadline] = []

    def add_deadline(self, deadline: Deadline) -> str:
        self._deadlines.append(deadline)
        return deadline.id

    def get_upcoming(self, days: int = 30) -> List[Deadline]:
        return self._deadlines[:5]

class TaskManager:
    def __init__(self, matter_id: str = "") -> None:
        self.matter_id = matter_id
        self._tasks: Dict[str, LegalTask] = {}

    def create_task(self, task: LegalTask) -> str:
        self._tasks[task.id] = task
        return task.id

class TimeTracker:
    def __init__(self, matter_id: str = "") -> None:
        self.matter_id = matter_id
        self._entries: List[TimeEntry] = []

    def log_time(self, entry: TimeEntry) -> str:
        self._entries.append(entry)
        return entry.id

    def get_total_hours(self, billable_only: bool = True) -> float:
        return sum(e.hours for e in self._entries if not billable_only or e.billable)

def main() -> None:
    print("=" * 60)
    print("  Case Management Module — Demo")
    print("=" * 60)

    manager = CaseManager()
    matter_id = manager.create_matter(Matter(matter_id="M-001", client="Acme Corp", matter_type="litigation", description="Contract dispute"))
    print(f"\n[+] Matter: {matter_id}")

    tracker = DeadlineTracker(matter_id)
    deadline_id = tracker.add_deadline(Deadline(description="Motion response", due_date="2024-02-15"))
    print(f"\n[+] Deadline: {deadline_id}")

    task_mgr = TaskManager(matter_id)
    task_id = task_mgr.create_task(LegalTask(title="Review contract", assignee="paralegal-001", priority=TaskPriority.HIGH))
    print(f"\n[+] Task: {task_id}")

    time_tracker = TimeTracker(matter_id)
    time_tracker.log_time(TimeEntry(attorney="jsmith@law.com", date="2024-01-15", hours=2.5, description="Contract review", billable=True))
    print(f"\n[+] Time: {time_tracker.get_total_hours()} billable hours")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

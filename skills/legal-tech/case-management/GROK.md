---
name: "case-management"
category: "legal-tech"
version: "2.0.0"
tags: ["legal", "case", "management", "litigation", "tracking"]
description: "Legal case management, tracking, and workflow automation"
---

# Case Management

## Overview

The Case Management module provides comprehensive tools for managing legal cases, tracking deadlines, organizing documents, and automating legal workflows. It supports matter management, deadline tracking, task assignment, billing integration, and reporting for law firms and legal departments.

## Core Capabilities

- **Matter Management**: Track all aspects of legal matters
- **Deadline Management**: Track court deadlines and statute of limitations
- **Task Management**: Assign and track legal tasks
- **Document Organization**: Organize case documents and exhibits
- **Time Tracking**: Track billable hours and expenses
- **Billing Integration**: Generate invoices from time entries
- **Calendar Integration**: Sync with calendar systems
- **Reporting**: Generate case and matter reports

## Usage Examples

### Matter Management

```python
from case_management import CaseManager, Matter

manager = CaseManager()

# Create matter
matter = Matter(
    matter_id="MATTER-2024-001",
    client="Acme Corporation",
    matter_type="litigation",
    description="Contract dispute with vendor",
    responsible_attorney="jsmith@lawfirm.com",
    status="active",
    opened_date="2024-01-15",
)

matter_id = manager.create_matter(matter)
print(f"Matter Created: {matter_id}")
print(f"  Client: {matter.client}")
print(f"  Type: {matter.matter_type}")
```

### Deadline Tracking

```python
from case_management import DeadlineTracker, Deadline

tracker = DeadlineTracker(matter_id="MATTER-2024-001")

# Add deadline
deadline = Deadline(
    description="Response to Motion to Dismiss",
    due_date="2024-02-15",
    deadline_type="court_filing",
    responsible_attorney="jsmith@lawfirm.com",
    alert_days_before=14,
)

deadline_id = tracker.add_deadline(deadline)
print(f"Deadline Added: {deadline_id}")
print(f"  Due: {deadline.due_date}")
```

### Task Management

```python
from case_management import TaskManager, LegalTask

task_mgr = TaskManager(matter_id="MATTER-2024-001")

# Create task
task = LegalTask(
    title="Review contract for discovery",
    assignee="paralegal-001",
    priority="high",
    due_date="2024-02-01",
    estimated_hours=8,
)

task_id = task_mgr.create_task(task)
print(f"Task Created: {task_id}")
```

### Time Tracking

```python
from case_management import TimeTracker, TimeEntry

tracker = TimeTracker(matter_id="MATTER-2024-001")

# Log time
entry = TimeEntry(
    attorney="jsmith@lawfirm.com",
    date="2024-01-15",
    hours=2.5,
    description="Review and analysis of contract",
    activity_type="research",
    billable=True,
)

entry_id = tracker.log_time(entry)
print(f"Time Logged: {entry.hours}h ({entry.activity_type})")
```

## Best Practices

- **Systematic Organization**: Organize matters consistently
- **Deadline Management**: Never miss court deadlines
- **Time Capture**: Capture time contemporaneously
- **Document Management**: Maintain organized document repositories
- **Communication Logging**: Log all client communications
- **Conflict Checks**: Conduct conflict checks before opening matters
- **Client Updates**: Provide regular client updates
- **Matter Closing**: Properly close and archive completed matters

## Related Modules

- **e-discovery**: Document discovery management
- **legal-research**: Research for case matters
- **compliance-tools**: Compliance tracking for matters

## Advanced Configuration

### Matter Configuration

```python
from case_management import MatterConfig, MatterType

config = MatterConfig(
    # Matter types
    matter_types={
        MatterType.LITIGATION: {
            "description": "Active litigation",
            "required_fields": ["court", "case_number", "judge"],
            "deadline_types": ["filing", "discovery", "trial"],
            "billing_required": True,
        },
        MatterType.TRANSACTION: {
            "description": "Business transaction",
            "required_fields": ["deal_type", "closing_date"],
            "deadline_types": ["due_diligence", "closing"],
            "billing_required": True,
        },
        MatterType.ADVISORY: {
            "description": "Legal advisory",
            "required_fields": ["requestor", "topic"],
            "deadline_types": ["response"],
            "billing_required": False,
        },
        MatterType.INVESTIGATION: {
            "description": "Internal investigation",
            "required_fields": ["investigation_type"],
            "deadline_types": ["report", "remediation"],
            "billing_required": False,
        },
    },
    # Matter numbering
    numbering={
        "prefix": "MATTER",
        "year_format": "YYYY",
        "sequence_length": 4,
        "separator": "-",
    },
    # Matter statuses
    statuses={
        "new": {"description": "New matter opened"},
        "active": {"description": "Matter in progress"},
        "pending": {"description": "Matter on hold"},
        "closed": {"description": "Matter completed"},
        "archived": {"description": "Matter archived"},
    },
)

manager = CaseManager(config)
```

### Deadline Configuration

```python
from case_management import DeadlineConfig, DeadlineType

deadline_config = DeadlineConfig(
    # Deadline types
    deadline_types={
        DeadlineType.COURT_FILING: {
            "description": "Court filing deadline",
            "calendar_days": True,
            "business_days": False,
            "alert_days": [30, 14, 7, 3, 1],
            "escalation_days": [14, 7, 3],
        },
        DeadlineType.DISCOVERY: {
            "description": "Discovery deadline",
            "calendar_days": True,
            "business_days": False,
            "alert_days": [14, 7, 3, 1],
            "escalation_days": [7, 3],
        },
        DeadlineType.STATUTE: {
            "description": "Statute of limitations",
            "calendar_days": True,
            "business_days": False,
            "alert_days": [90, 60, 30, 14, 7],
            "escalation_days": [30, 14, 7],
        },
        DeadlineType.CONTRACTUAL: {
            "description": "Contractual deadline",
            "calendar_days": False,
            "business_days": True,
            "alert_days": [10, 5, 2],
            "escalation_days": [5, 2],
        },
    },
    # Calendar integration
    calendar_sync={
        "sync_enabled": True,
        "sync_frequency": "hourly",
        "calendar_types": ["outlook", "google"],
        "reminder_defaults": {"days_before": 7},
    },
)

tracker = DeadlineTracker(deadline_config)
```

### Time Tracking Configuration

```python
from case_management import TimeTrackingConfig, ActivityType

time_config = TimeTrackingConfig(
    # Activity types
    activity_types={
        ActivityType.RESEARCH: {"description": "Legal research", "billable": True, "rate_multiplier": 1.0},
        ActivityType.DRAFTING: {"description": "Document drafting", "billable": True, "rate_multiplier": 1.0},
        ActivityType.REVIEW: {"description": "Document review", "billable": True, "rate_multiplier": 1.0},
        ActivityType.MEETING: {"description": "Client meeting", "billable": True, "rate_multiplier": 1.0},
        ActivityType.COURT: {"description": "Court appearance", "billable": True, "rate_multiplier": 1.5},
        ActivityType.TRAVEL: {"description": "Travel time", "billable": True, "rate_multiplier": 0.75},
        ActivityType.ADMIN: {"description": "Administrative", "billable": False, "rate_multiplier": 0},
    },
    # Billing rules
    billing_rules={
        "minimum_increment": 0.1,  # 6 minutes
        "rounding": "up",
        "description_required": True,
        "client_approval_required": False,
    },
    # Rate tables
    rate_tables={
        "standard": {
            "partner": 600,
            "associate": 350,
            "paralegal": 150,
        },
        "discounted": {
            "partner": 500,
            "associate": 300,
            "paralegal": 125,
        },
    },
)

tracker = TimeTracker(time_config)
```

## Architecture Patterns

### Case Management Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Case Management System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Matter  │──▶│ Deadline │──▶│  Task    │──▶│ Document │ │
│  │Management│   │ Tracking │   │Management│   │Management│ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ Client   │   │ Calendar │   │ Resource │   │  Billing │ │
│  │ Management│   │ Integration│  │ Allocation│  │Integration│ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Event-Driven Case System

```yaml
events:
  matter.created:
    description: "New matter created"
    payload:
      matter_id: "string"
      client: "string"
      matter_type: "string"
    handlers:
      - create_matter_workspace
      - notify_responsible_attorney
      - create_conflict_check

  deadline.upcoming:
    description: "Deadline approaching"
    payload:
      deadline_id: "string"
      days_remaining: "integer"
      matter_id: "string"
    handlers:
      - send_reminder
      - escalate_if_overdue

  task.completed:
    description: "Task completed"
    payload:
      task_id: "string"
      matter_id: "string"
      completed_by: "string"
    handlers:
      - update_task_status
      - notify_matter_team
      - check_matter_completion

  time.logged:
    description: "Time entry logged"
    payload:
      entry_id: "string"
      matter_id: "string"
      hours: "float"
      billable: "boolean"
    handlers:
      - update_matter_hours
      - update_billing
      - check_budget
```

### Data Flow Architecture

```python
from case_management import CaseManagementPipeline

class CaseManagementPipeline:
    def __init__(self):
        self.matter_manager = CaseManager()
        self.deadline_tracker = DeadlineTracker()
        self.task_manager = TaskManager()
        self.document_manager = DocumentManager()
        self.time_tracker = TimeTracker()

    async def open_matter(self, matter_data: MatterData):
        # Stage 1: Conflict check
        conflicts = await self.check_conflicts(matter_data)
        if conflicts:
            return {"error": "Conflicts detected", "conflicts": conflicts}

        # Stage 2: Create matter
        matter = await self.matter_manager.create(matter_data)

        # Stage 3: Set up deadlines
        deadlines = await self.deadline_tracker.setup_defaults(matter)

        # Stage 4: Create initial tasks
        tasks = await self.task_manager.create_initial_tasks(matter)

        # Stage 5: Set up document structure
        doc_structure = await self.document_manager.create_structure(matter)

        return {
            "matter": matter,
            "deadlines": deadlines,
            "tasks": tasks,
            "document_structure": doc_structure,
        }
```

## Integration Guide

### Calendar Integration

```python
from case_management import CalendarIntegration

calendar = CalendarIntegration(
    provider="outlook",
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Sync deadlines to calendar
async def sync_deadlines_to_calendar(matter_id: str):
    deadlines = await deadline_tracker.get_deadlines(matter_id)

    for deadline in deadlines:
        await calendar.create_event(
            summary=f"{deadline.description} - {deadline.matter_id}",
            start=deadline.due_date,
            end=deadline.due_date,
            reminder_days=deadline.alert_days_before,
            categories=["Legal", "Deadline"],
        )

# Sync court dates
async def sync_court_dates(matter_id: str):
    court_dates = await get_court_dates(matter_id)

    for court_date in court_dates:
        await calendar.create_event(
            summary=f"Court: {court_date.description}",
            start=court_date.date,
            end=court_date.date + timedelta(hours=2),
            location=court_date.court,
            categories=["Legal", "Court"],
        )
```

### Billing System Integration

```python
from case_management import BillingIntegration

billing = BillingIntegration(
    platform="quickbooks",
    api_key="your_api_key",
)

# Generate invoice
async def generate_invoice(matter_id: str, billing_period: str):
    time_entries = await time_tracker.get_entries(
        matter_id=matter_id,
        billing_period=billing_period,
        billable=True,
    )

    invoice = await billing.create_invoice(
        client=matter.client,
        entries=time_entries,
        rate_table=matter.rate_table,
    )

    return invoice

# Sync payments
async def sync_payments(matter_id: str):
    payments = await billing.get_payments(matter_id)
    await time_tracker.apply_payments(matter_id, payments)
```

### Document Management Integration

```python
from case_management import DMSIntegration

dms = DMSIntegration(
    provider="netdocuments",
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Create matter folder structure
async def create_matter_folders(matter_id: str):
    structure = {
        "Pleadings": [],
        "Discovery": [],
        "Correspondence": [],
        "Research": [],
        "Billing": [],
        "Exhibits": [],
    }

    await dms.create_folder_structure(
        parent_folder=f" Matters/{matter_id}",
        structure=structure,
    )

# Link documents to matter
async def link_document(matter_id: str, document_id: str):
    await dms.link_to_matter(
        document_id=document_id,
        matter_id=matter_id,
    )
```

## Performance Optimization

### Parallel Task Processing

```python
import asyncio
from case_management import ParallelTaskManager

task_mgr = ParallelTaskManager(max_concurrent=10)

async def parallel_task_assignment(tasks: list, assignees: list):
    """Assign multiple tasks in parallel."""
    semaphore = asyncio.Semaphore(10)

    async def assign_with_semaphore(task, assignee):
        async with semaphore:
            return await task_mgr.assign(task, assignee)

    assignment_tasks = [
        assign_with_semaphore(task, assignees[i % len(assignees)])
        for i, task in enumerate(tasks)
    ]

    results = await asyncio.gather(*assignment_tasks, return_exceptions=True)

    return {
        "assigned": len([r for r in results if not isinstance(r, Exception)]),
        "failed": len([r for r in results if isinstance(r, Exception)]),
    }
```

### Deadline Calculation Optimization

```python
from case_management import DeadlineOptimizer

optimizer = DeadlineOptimizer()

# Optimize deadline calculations
async def optimize_deadlines(matter_id: str):
    deadlines = await deadline_tracker.get_deadlines(matter_id)

    # Calculate optimal scheduling
    optimized = optimizer.optimize_schedule(
        deadlines=deadlines,
        resources=await get_available_resources(),
        court_calendar=await get_court_calendar(),
    )

    return optimized

# Batch deadline processing
async def batch_process_deadlines(matter_ids: list):
    """Process deadlines for multiple matters."""
    tasks = [optimize_deadlines(mid) for mid in matter_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results
```

### Report Generation Optimization

```python
from case_management import ReportOptimizer

report_optimizer = ReportOptimizer()

async def optimized_matter_report(matter_id: str):
    """Generate optimized matter report."""
    # Pre-fetch all data
    data = await report_optimizer.prefetch_matter_data(matter_id)

    # Generate sections in parallel
    sections = await report_optimizer.generate_sections_parallel(
        data=data,
        sections=["summary", "deadlines", "tasks", "billing", "documents"],
    )

    # Assemble final report
    report = await report_optimizer.assemble_report(sections)

    return report
```

## Security Considerations

### Matter Access Control

```python
from case_management import AccessControl, Permission

access_control = AccessControl()

# Define permissions
permissions = {
    "matter.read": "Read matter information",
    "matter.write": "Modify matter information",
    "matter.admin": "Administer matter settings",
    "deadline.read": "Read deadlines",
    "deadline.write": "Modify deadlines",
    "task.read": "Read tasks",
    "task.write": "Modify tasks",
    "time.read": "Read time entries",
    "time.write": "Log time entries",
    "billing.read": "Read billing information",
    "billing.write": "Modify billing",
}

# Role-based access
roles = {
    "partner": list(permissions.keys()),
    "associate": [
        "matter.read", "matter.write",
        "deadline.read", "deadline.write",
        "task.read", "task.write",
        "time.read", "time.write",
    ],
    "paralegal": [
        "matter.read",
        "deadline.read",
        "task.read", "task.write",
        "time.read", "time.write",
    ],
    "client": [
        "matter.read",
        "billing.read",
    ],
}

@access_control.require_permission("matter.write")
async def update_matter(matter_id: str, data: dict):
    """Update matter with access control."""
    return await manager.update(matter_id, data)
```

### Confidentiality Protection

```python
from case_management import ConfidentialityProtection

confidentiality = ConfidentialityProtection(
    classification_levels=["public", "internal", "confidential", "privileged"],
)

# Classify matter information
def classify_matter(matter: Matter) -> str:
    """Determine matter classification level."""
    if matter.contains_privileged_info:
        return "privileged"
    elif matter.confidential:
        return "confidential"
    elif matter.internal_only:
        return "internal"
    else:
        return "public"

# Protect privileged communications
@confidentiality.protect_privilege
async def access_communication(comm_id: str):
    """Access communication with privilege protection."""
    return await db.get_communication(comm_id)
```

### Audit Trail

```python
from case_management import CaseAuditTrail
from datetime import datetime

audit_trail = CaseAuditTrail(
    storage="database",
    retention_days=2555,
)

def log_case_action(
    action: str,
    user_id: str,
    matter_id: str,
    details: dict = None,
):
    """Log case-related action."""
    audit_trail.log(
        timestamp=datetime.utcnow(),
        action=action,
        user_id=user_id,
        resource_type="matter",
        resource_id=matter_id,
        ip_address=get_client_ip(),
        details=details or {},
    )

# Example usage
log_case_action(
    action="matter.created",
    user_id="user-001",
    matter_id="MATTER-2024-001",
    details={"client": "Acme Corp", "type": "litigation"},
)
```

## Troubleshooting Guide

### Common Issues

#### Issue: Deadline Missed

```python
# Symptom: Court deadline missed
# Diagnosis:
from case_management import DeadlineDiagnostics

diagnostics = DeadlineDiagnostics()

analysis = diagnostics.analyze_missed_deadline("deadline-001")
print(f"Deadline: {analysis.deadline_description}")
print(f"Due date: {analysis.due_date}")
print(f"Alerts sent: {analysis.alerts_sent}")
print(f"Acknowledgments: {analysis.acknowledgments}")

# Resolution:
# 1. Document the missed deadline
# 2. Notify responsible attorney
# 3. Assess impact
# 4. Take corrective action
```

#### Issue: Time Entry Discrepancies

```python
# Symptom: Billing time doesn't match records
# Diagnosis:
from case_management import TimeDiagnostics

time_diag = TimeDiagnostics()

analysis = time_diag.analyze_discrepancies("matter-001")
print(f"Total hours logged: {analysis.total_hours}")
print(f"Hours billed: {analysis.billed_hours}")
print(f"Discrepancies: {analysis.discrepancy_count}")
print(f"Common issues: {analysis.common_issues}")

# Resolution:
# 1. Review time entries
# 2. Identify discrepancies
# 3. Make corrections
# 4. Update billing
```

#### Issue: Task Bottleneck

```python
# Symptom: Tasks not progressing
# Diagnosis:
from case_management import TaskDiagnostics

task_diag = TaskDiagnostics()

analysis = task_diag.analyze_bottleneck("matter-001")
print(f"Overdue tasks: {analysis.overdue_count}")
print(f"Blocked tasks: {analysis.blocked_count}")
print(f"Resource utilization: {analysis.resource_utilization:.1%}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Reassign tasks
# 2. Remove blockers
# 3. Adjust priorities
# 4. Add resources
```

## API Reference

### Matter API

```python
# POST /api/v2/matters
# Create matter

@router.post("/matters")
async def create_matter(
    request: CreateMatterRequest,
) -> MatterResponse:
    """
    Create new matter.

    Args:
        request: Matter creation data

    Returns:
        MatterResponse with created matter
    """
    pass

# GET /api/v2/matters/{matter_id}
# Get matter

@router.get("/matters/{matter_id}")
async def get_matter(
    matter_id: str,
) -> MatterResponse:
    """
    Get matter details.

    Args:
        matter_id: Matter identifier

    Returns:
        MatterResponse with matter details
    """
    pass
```

### Deadline API

```python
# POST /api/v2/matters/{matter_id}/deadlines
# Add deadline

@router.post("/matters/{matter_id}/deadlines")
async def add_deadline(
    matter_id: str,
    request: AddDeadlineRequest,
) -> DeadlineResponse:
    """
    Add deadline to matter.

    Args:
        matter_id: Matter identifier
        request: Deadline data

    Returns:
        DeadlineResponse with added deadline
    """
    pass

# GET /api/v2/matters/{matter_id}/deadlines
# List deadlines

@router.get("/matters/{matter_id}/deadlines")
async def list_deadlines(
    matter_id: str,
    status: str = None,
) -> DeadlineListResponse:
    """
    List matter deadlines.

    Args:
        matter_id: Matter identifier
        status: Filter by status

    Returns:
        DeadlineListResponse with deadlines
    """
    pass
```

### Time Entry API

```python
# POST /api/v2/matters/{matter_id}/time
# Log time entry

@router.post("/matters/{matter_id}/time")
async def log_time(
    matter_id: str,
    request: LogTimeRequest,
) -> TimeEntryResponse:
    """
    Log time entry.

    Args:
        matter_id: Matter identifier
        request: Time entry data

    Returns:
        TimeEntryResponse with logged entry
    """
    pass

# GET /api/v2/matters/{matter_id}/time
# List time entries

@router.get("/matters/{matter_id}/time")
async def list_time_entries(
    matter_id: str,
    billing_period: str = None,
) -> TimeEntryListResponse:
    """
    List time entries.

    Args:
        matter_id: Matter identifier
        billing_period: Filter by billing period

    Returns:
        TimeEntryListResponse with entries
    """
    pass
```

## Data Models

### Matter Model

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
from enum import Enum

class MatterStatus(Enum):
    NEW = "new"
    ACTIVE = "active"
    PENDING = "pending"
    CLOSED = "closed"
    ARCHIVED = "archived"

@dataclass
class Matter:
    id: str
    matter_id: str
    client: str
    matter_type: str
    description: str
    responsible_attorney: str
    status: MatterStatus
    opened_date: date
    closed_date: Optional[date]
    court: Optional[str]
    case_number: Optional[str]
    judge: Optional[str]
    total_hours: float
    total_billed: float
    created_at: datetime
    updated_at: datetime
    created_by: str
    metadata: dict
```

### Deadline Model

```python
@dataclass
class Deadline:
    id: str
    matter_id: str
    description: str
    due_date: date
    deadline_type: str
    responsible_attorney: str
    alert_days_before: int
    status: str
    completed_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Task Model

```python
@dataclass
class LegalTask:
    id: str
    matter_id: str
    title: str
    description: str
    assignee: str
    priority: str
    due_date: date
    estimated_hours: float
    actual_hours: Optional[float]
    status: str
    completed_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    created_by: str
```

### Time Entry Model

```python
@dataclass
class TimeEntry:
    id: str
    matter_id: str
    attorney: str
    date: date
    hours: float
    description: str
    activity_type: str
    billable: bool
    billed: bool
    invoice_id: Optional[str]
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: case-management-api
  namespace: legal-tech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: case-management-api
  template:
    metadata:
      labels:
        app: case-management-api
    spec:
      containers:
      - name: case-management-api
        image: legal-tech/case-management:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: case-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

MATTERS_CREATED = Counter(
    'case_matters_created_total',
    'Total matters created',
    ['type']
)

DEADLINES_TRACKED = Counter(
    'case_deadlines_tracked_total',
    'Total deadlines tracked',
    ['status']
)

TIME_LOGGED = Counter(
    'case_time_logged_total',
    'Total hours logged',
    ['activity_type']
)

TASKS_COMPLETED = Counter(
    'case_tasks_completed_total',
    'Total tasks completed'
)
```

### Logging Configuration

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "matter_id": getattr(record, "matter_id", None),
            "user_id": getattr(record, "user_id", None),
        }
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger("case_management")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger
```

## Testing Strategy

### Unit Tests

```python
import pytest
from case_management import CaseManager, DeadlineTracker

class TestCaseManager:
    def setup_method(self):
        self.manager = CaseManager()

    def test_create_matter(self):
        """Test matter creation."""
        matter = Matter(
            matter_id="MATTER-001",
            client="Test Client",
            matter_type="litigation",
            description="Test matter",
        )
        result = self.manager.create_matter(matter)
        assert result.id is not None
        assert result.status == MatterStatus.NEW
```

### Integration Tests

```python
import pytest
from httpx import AsyncClient
from case_management import app

@pytest.mark.asyncio
class TestCaseAPI:
    async def test_create_matter(self, async_client: AsyncClient):
        """Test matter creation endpoint."""
        response = await async_client.post(
            "/api/v2/matters",
            json={
                "client": "Test Client",
                "matter_type": "litigation",
                "description": "Test matter",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["client"] == "Test Client"
```

## Versioning & Migration

### API Versioning

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.post("/matters")
async def create_matter_v1():
    pass

@v2_router.post("/matters")
async def create_matter_v2(request: CreateMatterRequest):
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

### Database Migrations

```python
# migrations/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'matters',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('matter_id', sa.String(50), nullable=False),
        sa.Column('client', sa.String(200), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('opened_date', sa.Date, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('matters')
```

## Glossary

### Case Management Terms

| Term | Definition |
|------|------------|
| **Matter** | Legal case or engagement |
| **Deadline** | Date by which action must be taken |
| **Task** | Specific work item within a matter |
| **Time Entry** | Record of billable/non-billable time |
| **Billing** | Process of invoicing for legal services |
| **Conflict Check** | Verification of no conflicts of interest |
| **Statute of Limitations** | Deadline for filing legal action |
| **Court Filing** | Document submitted to court |
| **Client Communication** | Correspondence with client |
| **Matter Closing** | Completion and archival of matter |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added AI-powered matter management
- Implemented parallel task processing
- Enhanced deadline tracking
- Added billing integration

### Version 1.5.0 (2023-10-01)
- Added time tracking
- Implemented task management
- Enhanced reporting
- Added calendar integration

### Version 1.4.0 (2023-07-15)
- Added document management
- Implemented deadline tracking
- Added matter tracking
- Enhanced security

### Version 1.3.0 (2023-04-01)
- Added matter management
- Implemented client management
- Added conflict checking
- Enhanced API

### Version 1.2.0 (2023-01-15)
- Added basic matter tracking
- Implemented deadline management
- Added task creation
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added matter creation
- Implemented basic tracking
- Added reporting
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic case management
- REST API
- PostgreSQL support

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/company/case-management.git
cd case-management
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
uvicorn main:app --reload
```

### Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings
- Maintain 80% test coverage
- Run linting before commit

## License

MIT License

Copyright (c) 2024 Case Management Contributors

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

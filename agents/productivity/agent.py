#!/usr/bin/env python3
"""
Grok Productivity Agent
Specialized agent for productivity optimization, task management, and workflow automation.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    created_at: datetime
    due_date: Optional[datetime]
    estimated_hours: float
    tags: List[str]
    dependencies: List[str]
    context: Dict[str, Any]

@dataclass
class ProductivityMetrics:
    tasks_completed: int
    total_hours_logged: float
    average_task_completion_time: float
    blocked_tasks_count: int
    productivity_score: float

class TaskManager:
    """Manages task creation, tracking, and organization."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_graph = {}
        self.calendar = {}
    
    def create_task(self, title: str, description: str,
                   priority: Priority, due_date: Optional[datetime] = None,
                   estimated_hours: float = 1.0, tags: List[str] = None,
                   dependencies: List[str] = None) -> Task:
        """Create and register a new task."""
        task = Task(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
            created_at=datetime.now(),
            due_date=due_date,
            estimated_hours=estimated_hours,
            tags=tags or [],
            dependencies=dependencies or [],
            context={}
        )
        self.tasks[task.id] = task
        
        if dependencies:
            for dep_id in dependencies:
                if dep_id in self.task_graph:
                    self.task_graph[dep_id].append(task.id)
                else:
                    self.task_graph[dep_id] = [task.id]
        
        return task
    
    def update_task(self, task_id: str, **updates) -> Task:
        """Update task properties."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        return task
    
    def complete_task(self, task_id: str, hours_logged: float = None) -> Task:
        """Mark task as completed."""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.context['completed_at'] = datetime.now()
            if hours_logged:
                task.context['hours_logged'] = hours_logged
        return task
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with specified status."""
        return [t for t in self.tasks.values() if t.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get all tasks with specified priority."""
        return [t for t in self.tasks.values() if t.priority == priority]
    
    def get_critical_path(self) -> List[Task]:
        """Calculate critical path through task dependencies."""
        completed = {t.id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED}
        
        def calculate_depth(task_id: str, visited: set) -> int:
            if task_id in visited:
                return 0
            visited.add(task_id)
            
            dependencies = self.task_graph.get(task_id, [])
            if not dependencies:
                return 1
            
            max_depth = 0
            for dep_id in dependencies:
                if dep_id not in completed:
                    depth = calculate_depth(dep_id, visited.copy())
                    max_depth = max(max_depth, depth)
            
            return max_depth + 1
        
        task_depths = [(t.id, calculate_depth(t.id, set())) for t in self.tasks.values()]
        sorted_ids = [tid for tid, _ in sorted(task_depths, key=lambda x: -x[1])]
        
        return [self.tasks[tid] for tid in sorted_ids if tid in self.tasks]
    
    def detect_blockers(self) -> List[Task]:
        """Identify blocked tasks."""
        blocked = []
        for task in self.tasks.values():
            if task.status == TaskStatus.BLOCKED:
                blocked.append(task)
            elif task.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]:
                for dep_id in task.dependencies:
                    dep_task = self.tasks.get(dep_id)
                    if dep_task and dep_task.status != TaskStatus.COMPLETED:
                        task.status = TaskStatus.BLOCKED
                        blocked.append(task)
                        break
        return blocked

class TimeTracker:
    """Tracks time spent on tasks and activities."""
    
    def __init__(self):
        self.sessions = []
        self.current_session = None
    
    def start_session(self, task_id: str) -> None:
        """Start tracking time for a task."""
        self.current_session = {
            'task_id': task_id,
            'start_time': datetime.now(),
            'end_time': None,
            'breaks': []
        }
    
    def end_session(self) -> Dict[str, Any]:
        """End current tracking session."""
        if self.current_session:
            self.current_session['end_time'] = datetime.now()
            duration = (self.current_session['end_time'] - 
                       self.current_session['start_time']).total_seconds() / 3600
            self.current_session['duration_hours'] = duration
            self.sessions.append(self.current_session)
            self.current_session = None
        return self.current_session or {}
    
    def log_break(self, duration_minutes: int) -> None:
        """Log a break during current session."""
        if self.current_session:
            self.current_session['breaks'].append({
                'start': datetime.now(),
                'duration_minutes': duration_minutes
            })
    
    def get_daily_report(self, date: datetime = None) -> Dict[str, Any]:
        """Generate daily productivity report."""
        date = date or datetime.now()
        day_sessions = [s for s in self.sessions 
                       if s['start_time'].date() == date.date()]
        
        total_hours = sum(s.get('duration_hours', 0) for s in day_sessions)
        task_hours = {}
        for s in day_sessions:
            task_id = s['task_id']
            if task_id in task_hours:
                task_hours[task_id] += s.get('duration_hours', 0)
            else:
                task_hours[task_id] = s.get('duration_hours', 0)
        
        return {
            'date': date.date().isoformat(),
            'total_hours': total_hours,
            'sessions_count': len(day_sessions),
            'task_breakdown': task_hours
        }

class ProductivityOptimizer:
    """Optimizes productivity using data-driven insights."""
    
    def __init__(self, task_manager: TaskManager, time_tracker: TimeTracker):
        self.task_manager = task_manager
        self.time_tracker = time_tracker
    
    def calculate_metrics(self) -> ProductivityMetrics:
        """Calculate productivity metrics."""
        completed = self.task_manager.get_tasks_by_status(TaskStatus.COMPLETED)
        blocked = self.task_manager.get_tasks_by_status(TaskStatus.BLOCKED)
        
        total_hours = sum(
            t.context.get('hours_logged', t.estimated_hours)
            for t in completed
        )
        
        completion_times = []
        for t in completed:
            if 'completed_at' in t.context and t.created_at:
                duration = (t.context['completed_at'] - t.created_at).total_seconds() / 3600
                completion_times.append(duration)
        
        avg_completion = sum(completion_times) / len(completion_times) if completion_times else 0
        
        if completed:
            planned_hours = sum(t.estimated_hours for t in completed)
            efficiency = planned_hours / total_hours if total_hours > 0 else 1.0
            productivity_score = min(1.0, efficiency) * 100
        else:
            productivity_score = 0
        
        return ProductivityMetrics(
            tasks_completed=len(completed),
            total_hours_logged=total_hours,
            average_task_completion_time=avg_completion,
            blocked_tasks_count=len(blocked),
            productivity_score=productivity_score
        )
    
    def suggest_schedule(self, available_hours: float = 8.0) -> List[Task]:
        """Suggest optimal task schedule for available time."""
        high_priority = self.task_manager.get_tasks_by_priority(Priority.CRITICAL)
        high_priority.extend(self.task_manager.get_tasks_by_priority(Priority.HIGH))
        
        scheduled = []
        remaining_hours = available_hours
        
        for task in sorted(high_priority, key=lambda t: t.priority.value):
            if remaining_hours >= task.estimated_hours:
                scheduled.append(task)
                remaining_hours -= task.estimated_hours
        
        return scheduled
    
    def identify_bottlenecks(self) -> Dict[str, Any]:
        """Identify productivity bottlenecks."""
        metrics = self.calculate_metrics()
        blocked = self.task_manager.detect_blockers()
        
        bottlenecks = []
        if metrics.blocked_tasks_count > 3:
            bottlenecks.append("High number of blocked tasks")
        
        if metrics.productivity_score < 50:
            bottlenecks.append("Low productivity score")
        
        by_priority = {}
        for task in blocked:
            if task.priority in by_priority:
                by_priority[task.priority].append(task.id)
            else:
                by_priority[task.priority] = [task.id]
        
        return {
            'bottlenecks': bottlenecks,
            'blocked_by_priority': {p.name: len(ids) for p, ids in by_priority.items()},
            'recommendations': self._generate_recommendations(bottlenecks)
        }
    
    def _generate_recommendations(self, bottlenecks: List[str]) -> List[str]:
        """Generate recommendations based on bottlenecks."""
        recommendations = []
        if "High number of blocked tasks" in bottlenecks:
            recommendations.append("Review and resolve blocked tasks first")
            recommendations.append("Consider breaking large tasks into smaller ones")
        if "Low productivity score" in bottlenecks:
            recommendations.append("Focus on single-tasking")
            recommendations.append("Use time-blocking technique")
            recommendations.append("Minimize distractions during focus periods")
        return recommendations

class ProductivityAgent:
    """Main productivity agent."""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.time_tracker = TimeTracker()
        self.optimizer = ProductivityOptimizer(self.task_manager, self.time_tracker)
        self.workflows = {}
    
    def plan_day(self, tasks: List[Dict[str, Any]], 
                available_hours: float = 8.0) -> Dict[str, Any]:
        """Plan day's work."""
        created_tasks = []
        for task_data in tasks:
            task = self.task_manager.create_task(
                title=task_data['title'],
                description=task_data.get('description', ''),
                priority=Priority[task_data['priority'].upper()],
                due_date=task_data.get('due_date'),
                estimated_hours=task_data.get('estimated_hours', 1.0),
                tags=task_data.get('tags', []),
                dependencies=task_data.get('dependencies', [])
            )
            created_tasks.append(task)
        
        schedule = self.optimizer.suggest_schedule(available_hours)
        
        return {
            'tasks_created': len(created_tasks),
            'scheduled_tasks': [t.id for t in schedule],
            'total_estimated_hours': sum(t.estimated_hours for t in schedule),
            'available_hours': available_hours
        }
    
    def execute_workflow(self, workflow_name: str, task_ids: List[str]) -> Dict[str, Any]:
        """Execute productivity workflow."""
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            return {'error': f'Workflow {workflow_name} not found'}
        
        results = []
        for task_id in task_ids:
            task = self.task_manager.tasks.get(task_id)
            if task:
                self.time_tracker.start_session(task_id)
                task.status = TaskStatus.IN_PROGRESS
                results.append(task_id)
        
        return {
            'workflow': workflow_name,
            'tasks_started': results,
            'count': len(results)
        }
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get productivity dashboard data."""
        metrics = self.optimizer.calculate_metrics()
        blockers = self.task_manager.detect_blockers()
        bottlenecks = self.optimizer.identify_bottlenecks()
        
        return {
            'metrics': {
                'tasks_completed': metrics.tasks_completed,
                'total_hours': metrics.total_hours_logged,
                'productivity_score': metrics.productivity_score
            },
            'task_status': {
                'todo': len(self.task_manager.get_tasks_by_status(TaskStatus.TODO)),
                'in_progress': len(self.task_manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)),
                'completed': len(self.task_manager.get_tasks_by_status(TaskStatus.COMPLETED)),
                'blocked': len(blockers)
            },
            'recommendations': bottlenecks.get('recommendations', [])
        }

def main():
    """Main entry point."""
    agent = ProductivityAgent()
    
    tasks = [
        {'title': 'Code review', 'priority': 'HIGH', 'estimated_hours': 2.0},
        {'title': 'Write tests', 'priority': 'MEDIUM', 'estimated_hours': 3.0},
        {'title': 'Documentation', 'priority': 'LOW', 'estimated_hours': 1.0}
    ]
    
    plan = agent.plan_day(tasks, available_hours=8.0)
    dashboard = agent.get_dashboard()
    
    print(f"Day planned: {plan}")
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

"""
Automation Agent
Workflow automation and task orchestration
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import time
import json


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    task_id: str
    name: str
    action: str
    params: Dict
    status: WorkflowStatus
    depends_on: List[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 300
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


@dataclass
class Workflow:
    workflow_id: str
    name: str
    tasks: List[Task]
    status: WorkflowStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]


class WorkflowEngine:
    """Workflow execution engine"""
    
    def __init__(self):
        self.workflows = {}
        self.task_handlers = {}
        self.execution_history = []
    
    def register_handler(self, action: str, handler: Callable):
        """Register task handler"""
        self.task_handlers[action] = handler
    
    def create_workflow(self, name: str, tasks: List[Dict]) -> str:
        """Create new workflow"""
        workflow_id = f"wf_{int(time.time())}"
        
        task_objects = []
        for i, task_dict in enumerate(tasks):
            task_objects.append(Task(
                task_id=f"task_{i}",
                name=task_dict["name"],
                action=task_dict["action"],
                params=task_dict.get("params", {}),
                status=WorkflowStatus.PENDING,
                depends_on=task_dict.get("depends_on", []),
                max_retries=task_dict.get("max_retries", 3)
            ))
        
        self.workflows[workflow_id] = Workflow(
            workflow_id=workflow_id,
            name=name,
            tasks=task_objects,
            status=WorkflowStatus.PENDING,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None,
            error=None
        )
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str) -> Dict:
        """Execute workflow"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        completed = set()
        results = {}
        
        for task in workflow.tasks:
            if task.status == WorkflowStatus.COMPLETED:
                completed.add(task.task_id)
        
        max_iterations = len(workflow.tasks) * 3
        iterations = 0
        
        while len(completed) < len(workflow.tasks) and iterations < max_iterations:
            iterations += 1
            
            for task in workflow.tasks:
                if task.task_id in completed:
                    continue
                
                if not self._can_execute(task, completed):
                    continue
                
                try:
                    result = self._execute_task(task)
                    task.status = WorkflowStatus.COMPLETED
                    results[task.task_id] = result
                    completed.add(task.task_id)
                except Exception as e:
                    task.retry_count += 1
                    if task.retry_count >= task.max_retries:
                        task.status = WorkflowStatus.FAILED
                        workflow.status = WorkflowStatus.FAILED
                        workflow.error = str(e)
                        return {"error": str(e)}
        
        workflow.status = WorkflowStatus.COMPLETED
        workflow.completed_at = datetime.now()
        
        self.execution_history.append({
            "workflow_id": workflow_id,
            "status": workflow.status,
            "duration": (workflow.completed_at - workflow.started_at).total_seconds()
        })
        
        return {"status": "completed", "results": results}
    
    def _can_execute(self, task: Task, completed: set) -> bool:
        """Check if task can execute"""
        return all(dep in completed for dep in task.depends_on)
    
    def _execute_task(self, task: Task) -> Dict:
        """Execute single task"""
        if task.action not in self.task_handlers:
            raise ValueError(f"No handler for action: {task.action}")
        
        handler = self.task_handlers[task.action]
        return handler(task.params)
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get workflow status"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "completed_tasks": sum(1 for t in workflow.tasks if t.status == WorkflowStatus.COMPLETED),
            "total_tasks": len(workflow.tasks),
            "duration": (workflow.completed_at - workflow.started_at).total_seconds() if workflow.completed_at else None
        }


class ScheduleManager:
    """Task scheduling"""
    
    def __init__(self):
        self.schedules = {}
        self.jobs = {}
    
    def add_schedule(self,
                    name: str,
                    cron_expression: str,
                    workflow_id: str,
                    params: Dict = None):
        """Add scheduled task"""
        schedule_id = f"schedule_{int(time.time())}"
        self.schedules[schedule_id] = {
            "name": name,
            "cron": cron_expression,
            "workflow_id": workflow_id,
            "params": params or {},
            "enabled": True,
            "last_run": None,
            "next_run": self._parse_cron(cron_expression)
        }
    
    def _parse_cron(self, cron: str) -> datetime:
        """Parse cron expression (simplified)"""
        return datetime.now() + datetime.timedelta(minutes=5)
    
    def run_scheduled_jobs(self):
        """Run due scheduled jobs"""
        now = datetime.now()
        
        for schedule_id, schedule in self.schedules.items():
            if not schedule["enabled"]:
                continue
            
            if schedule["next_run"] and schedule["next_run"] <= now:
                self._execute_schedule(schedule_id)
    
    def _execute_schedule(self, schedule_id: str):
        """Execute scheduled job"""
        schedule = self.schedules[schedule_id]
        
        schedule["last_run"] = datetime.now()
        schedule["next_run"] = self._parse_cron(schedule["cron"])


class EmailAutomation:
    """Email automation"""
    
    def __init__(self):
        self.templates = {}
        self.campaigns = {}
    
    def create_template(self,
                       name: str,
                       subject: str,
                       body: str,
                       variables: List[str] = None):
        """Create email template"""
        self.templates[name] = {
            "subject": subject,
            "body": body,
            "variables": variables or []
        }
    
    def send_email(self,
                  to: str,
                  template: str,
                  variables: Dict = None) -> Dict:
        """Send email"""
        if template not in self.templates:
            raise ValueError(f"Template not found: {template}")
        
        tmpl = self.templates[template]
        subject = self._render_template(tmpl["subject"], variables)
        body = self._render_template(tmpl["body"], variables)
        
        return {
            "status": "sent",
            "to": to,
            "subject": subject,
            "timestamp": datetime.now()
        }
    
    def _render_template(self, template: str, variables: Dict = None) -> str:
        """Render template with variables"""
        if not variables:
            return template
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{{ {key} }}}}", str(value))
        return result
    
    def create_campaign(self,
                       name: str,
                       template: str,
                       recipients: List[str],
                       schedule: datetime = None):
        """Create email campaign"""
        campaign_id = f"campaign_{int(time.time())}"
        self.campaigns[campaign_id] = {
            "name": name,
            "template": template,
            "recipients": recipients,
            "schedule": schedule,
            "status": "draft"
        }
        return campaign_id
    
    def run_campaign(self, campaign_id: str) -> Dict:
        """Run email campaign"""
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign not found: {campaign_id}")
        
        campaign = self.campaigns[campaign_id]
        campaign["status"] = "running"
        
        results = []
        for recipient in campaign["recipients"]:
            result = self.send_email(recipient, campaign["template"])
            results.append(result)
        
        campaign["status"] = "completed"
        return {"sent": len(results), "results": results}


class FileAutomation:
    """File operations automation"""
    
    def __init__(self):
        self.watch_folders = {}
    
    def watch_folder(self, 
                    path: str,
                    extensions: List[str],
                    action: str):
        """Set up folder watcher"""
        self.watch_folders[path] = {
            "extensions": extensions,
            "action": action,
            "last_check": None
        }
    
    def process_files(self, 
                     path: str,
                     operation: str,
                     target: str = None) -> Dict:
        """Process files in folder"""
        import os
        results = {"processed": 0, "failed": 0, "files": []}
        
        try:
            files = os.listdir(path)
            for filename in files:
                try:
                    if operation == "move" and target:
                        os.rename(os.path.join(path, filename), target)
                    elif operation == "delete":
                        os.remove(os.path.join(path, filename))
                    results["processed"] += 1
                    results["files"].append(filename)
                except Exception as e:
                    results["failed"] += 1
        except Exception as e:
            results["error"] = str(e)
        
        return results


if __name__ == "__main__":
    engine = WorkflowEngine()
    scheduler = ScheduleManager()
    email = EmailAutomation()
    files = FileAutomation()
    
    engine.register_handler("send_email", lambda p: {"sent": True})
    engine.register_handler("api_call", lambda p: {"status": "ok"})
    
    workflow_id = engine.create_workflow("Example Workflow", [
        {"name": "Send Email", "action": "send_email", "params": {"to": "test@example.com"}},
        {"name": "API Call", "action": "api_call", "params": {"url": "https://api.example.com"}}
    ])
    
    result = engine.execute_workflow(workflow_id)
    status = engine.get_workflow_status(workflow_id)
    
    email.create_template("Welcome", "Welcome {{name}}", "Hello {{name}}!", ["name"])
    email.send_email("user@example.com", "Welcome", {"name": "John"})
    
    file_result = files.process_files("/tmp", "delete")
    
    print(f"Workflow ID: {workflow_id}")
    print(f"Workflow status: {status}")
    print(f"Email sent: {email}")
    print(f"Files processed: {file_result}")

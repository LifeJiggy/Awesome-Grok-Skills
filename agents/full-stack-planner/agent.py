"""
Full-Stack Planner Agent
Complete project planning and architecture
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class ProjectPhase(Enum):
    DISCOVERY = "discovery"
    DESIGN = "design"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"


class ArchitecturePattern(Enum):
    MONOLITHIC = "monolithic"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"


@dataclass
class ProjectPlan:
    project_id: str
    name: str
    description: str
    architecture: ArchitecturePattern
    phases: List[Dict]
    timeline_weeks: int
    budget: float
    team_size: int


class ProjectPlanner:
    """Project planning and estimation"""
    
    def __init__(self):
        self.projects = {}
        self.templates = {}
    
    def create_project(self, name: str, description: str, 
                      architecture: ArchitecturePattern) -> str:
        """Create new project plan"""
        project_id = f"proj_{len(self.projects) + 1}"
        
        self.projects[project_id] = {
            "id": project_id,
            "name": name,
            "description": description,
            "architecture": architecture,
            "phases": [],
            "status": "planning",
            "created_at": datetime.now()
        }
        
        return project_id
    
    def add_phase(self, project_id: str, phase: ProjectPhase, 
                  tasks: List[str], duration_weeks: int = 2) -> Dict:
        """Add project phase"""
        if project_id not in self.projects:
            return {"error": "Project not found"}
        
        phase_data = {
            "phase": phase.value,
            "tasks": tasks,
            "duration_weeks": duration_weeks,
            "status": "pending",
            "dependencies": []
        }
        
        self.projects[project_id]["phases"].append(phase_data)
        return phase_data
    
    def estimate_timeline(self, project_id: str, team_size: int = 1) -> Dict:
        """Estimate project timeline"""
        if project_id not in self.projects:
            return {"error": "Project not found"}
        
        project = self.projects[project_id]
        total_weeks = sum(p["duration_weeks"] for p in project["phases"])
        parallel_weeks = self._calculate_parallel_weeks(project["phases"], team_size)
        
        return {
            "project_id": project_id,
            "total_weeks": total_weeks,
            "optimized_weeks": parallel_weeks,
            "estimated_completion": datetime.now() + timedelta(weeks=parallel_weeks),
            "phases": [
                {"phase": p["phase"], "weeks": p["duration_weeks"]}
                for p in project["phases"]
            ]
        }
    
    def _calculate_parallel_weeks(self, phases: List[Dict], team_size: int) -> int:
        """Calculate optimized timeline with parallel work"""
        if team_size == 1:
            return sum(p["duration_weeks"] for p in phases)
        return int(sum(p["duration_weeks"] for p in phases) / team_size * 0.7)
    
    def generate_project_plan(self, project_id: str) -> ProjectPlan:
        """Generate complete project plan"""
        if project_id not in self.projects:
            raise ValueError("Project not found")
        
        project = self.projects[project_id]
        
        return ProjectPlan(
            project_id=project_id,
            name=project["name"],
            description=project["description"],
            architecture=project["architecture"],
            phases=project["phases"],
            timeline_weeks=sum(p["duration_weeks"] for p in project["phases"]),
            budget=50000,
            team_size=3
        )


class ArchitectureDesigner:
    """System architecture design"""
    
    def __init__(self):
        self.diagrams = {}
        self.components = {}
    
    def add_component(self, name: str, component_type: str, 
                     dependencies: List[str] = None) -> Dict:
        """Add architecture component"""
        self.components[name] = {
            "type": component_type,
            "dependencies": dependencies or [],
            "technologies": []
        }
        return self.components[name]
    
    def design_architecture(self, pattern: ArchitecturePattern) -> Dict:
        """Generate architecture design"""
        if pattern == ArchitecturePattern.MICROSERVICES:
            return self._design_microservices()
        elif pattern == ArchitecturePattern.SERVERLESS:
            return self._design_serverless()
        elif pattern == ArchitecturePattern.EVENT_DRIVEN:
            return self._design_event_driven()
        else:
            return self._design_monolithic()
    
    def _design_microservices(self) -> Dict:
        """Design microservices architecture"""
        return {
            "pattern": "microservices",
            "components": [
                {"name": "API Gateway", "type": "gateway"},
                {"name": "User Service", "type": "service"},
                {"name": "Order Service", "type": "service"},
                {"name": "Payment Service", "type": "service"},
                {"name": "Notification Service", "type": "service"},
                {"name": "PostgreSQL", "type": "database"},
                {"name": "Redis", "type": "cache"},
                {"name": "Kafka", "type": "message_queue"}
            ],
            "infrastructure": ["Kubernetes", "Docker", "Helm"],
            "communication": ["REST", "gRPC", "Kafka"]
        }
    
    def _design_serverless(self) -> Dict:
        """Design serverless architecture"""
        return {
            "pattern": "serverless",
            "components": [
                {"name": "CloudFront", "type": "cdn"},
                {"name": "API Gateway", "type": "gateway"},
                {"name": "Lambda Functions", "type": "functions"},
                {"name": "DynamoDB", "type": "database"},
                {"name": "S3", "type": "storage"},
                {"name": "Cognito", "type": "auth"}
            ],
            "infrastructure": ["AWS Lambda", "DynamoDB", "API Gateway"],
            "communication": ["REST", "WebSockets"]
        }
    
    def _design_event_driven(self) -> Dict:
        """Design event-driven architecture"""
        return {
            "pattern": "event_driven",
            "components": [
                {"name": "Event Producer", "type": "producer"},
                {"name": "Event Consumer", "type": "consumer"},
                {"name": "Message Broker", "type": "broker"},
                {"name": "Stream Processor", "type": "processor"},
                {"name": "Data Lake", "type": "storage"}
            ],
            "infrastructure": ["Kafka", "Debezium", "Spark"],
            "communication": ["Events", "Streams"]
        }
    
    def _design_monolithic(self) -> Dict:
        """Design monolithic architecture"""
        return {
            "pattern": "monolithic",
            "components": [
                {"name": "Web Server", "type": "server"},
                {"name": "Application Server", "type": "app"},
                {"name": "Database", "type": "database"},
                {"name": "File Storage", "type": "storage"}
            ],
            "infrastructure": ["Nginx", "PostgreSQL", "Redis"],
            "communication": ["HTTP", "Internal API"]
        }


class TechStackRecommender:
    """Technology stack recommendations"""
    
    def __init__(self):
        self.recommendations = {}
    
    def recommend_stack(self, project_type: str, 
                       scale_requirements: str = "medium") -> Dict:
        """Recommend technology stack"""
        stacks = {
            "web_application": {
                "frontend": ["React", "Vue.js", "Next.js"],
                "backend": ["Node.js", "Python/Django", "Go"],
                "database": ["PostgreSQL", "MongoDB"],
                "infrastructure": ["AWS", "Vercel", "Railway"]
            },
            "mobile_application": {
                "frontend": ["React Native", "Flutter", "Swift/Kotlin"],
                "backend": ["Node.js", "Python", "Firebase"],
                "database": ["PostgreSQL", "Firestore"],
                "infrastructure": ["AWS", "Firebase", "Vercel"]
            },
            "api_service": {
                "backend": ["FastAPI", "Express", "Go/Gin"],
                "database": ["PostgreSQL", "MySQL", "DynamoDB"],
                "cache": ["Redis", "Memcached"],
                "infrastructure": ["AWS Lambda", "Docker", "Kubernetes"]
            },
            "data_pipeline": {
                "processing": ["Apache Spark", "dbt", "Airflow"],
                "storage": ["Snowflake", "BigQuery", "PostgreSQL"],
                "infrastructure": ["AWS Glue", "Databricks", "Kubernetes"]
            }
        }
        
        project_rec = stacks.get(project_type, stacks["web_application"])
        
        scale_multiplier = {"small": 0.8, "medium": 1.0, "large": 1.5}.get(scale_requirements, 1.0)
        
        return {
            "project_type": project_type,
            "scale": scale_requirements,
            "stack": project_rec,
            "estimated_cost_per_month": round(1000 * scale_multiplier, 2),
            "complexity": "low" if scale_requirements == "small" else "medium" if scale_requirements == "medium" else "high"
        }


class RiskAssessor:
    """Project risk assessment"""
    
    def __init__(self):
        self.risks = []
    
    def assess_risks(self, project_plan: Dict) -> List[Dict]:
        """Assess project risks"""
        risks = [
            {
                "id": 1,
                "category": "Technical",
                "description": "Integration complexity between services",
                "likelihood": "medium",
                "impact": "high",
                "mitigation": "Use well-defined APIs and contract testing"
            },
            {
                "id": 2,
                "category": "Schedule",
                "description": "Feature creep during development",
                "likelihood": "high",
                "impact": "medium",
                "mitigation": "Strict scope management and prioritization"
            },
            {
                "id": 3,
                "category": "Resource",
                "description": "Key team member departure",
                "likelihood": "low",
                "impact": "high",
                "mitigation": "Cross-training and documentation"
            },
            {
                "id": 4,
                "category": "Technical",
                "description": "Performance at scale",
                "likelihood": "low",
                "impact": "high",
                "mitigation": "Load testing and horizontal scaling design"
            }
        ]
        
        self.risks = risks
        return risks
    
    def get_risk_summary(self) -> Dict:
        """Get risk summary"""
        high_risks = [r for r in self.risks if r["impact"] == "high"]
        return {
            "total_risks": len(self.risks),
            "high_priority": len(high_risks),
            "risk_items": high_risks
        }


class SprintPlanner:
    """Agile sprint planning"""
    
    def __init__(self):
        self.sprints = []
    
    def create_sprint(self, sprint_number: int, 
                     user_stories: List[Dict], duration: int = 2) -> Dict:
        """Create sprint plan"""
        sprint = {
            "number": sprint_number,
            "duration_weeks": duration,
            "stories": user_stories,
            "total_points": sum(s.get("points", 0) for s in user_stories),
            "capacity_points": duration * 10,
            "start_date": datetime.now() + timedelta(weeks=sprint_number * duration),
            "status": "planned"
        }
        
        self.sprints.append(sprint)
        return sprint
    
    def assign_story_points(self, stories: List[Dict]) -> List[Dict]:
        """Assign story points to user stories"""
        for story in stories:
            complexity = story.get("complexity", "medium")
            story["points"] = {"small": 2, "medium": 5, "large": 8, "epic": 13}.get(complexity, 5)
        return stories
    
    def generate_sprint_backlog(self, sprint_id: int) -> Dict:
        """Generate sprint backlog"""
        if sprint_id <= len(self.sprints):
            sprint = self.sprints[sprint_id - 1]
            return {
                "sprint_number": sprint["number"],
                "capacity": sprint["capacity_points"],
                "committed_points": sprint["total_points"],
                "stories": sprint["stories"]
            }
        return {"error": "Sprint not found"}


if __name__ == "__main__":
    planner = ProjectPlanner()
    project_id = planner.create_project("E-commerce Platform", "Full-featured e-commerce", ArchitecturePattern.MICROSERVICES)
    planner.add_phase(project_id, ProjectPhase.DISCOVERY, ["User research", "Requirements"], 2)
    planner.add_phase(project_id, ProjectPhase.DESIGN, ["UI/UX", "Architecture"], 3)
    planner.add_phase(project_id, ProjectPhase.DEVELOPMENT, ["Frontend", "Backend", "Integration"], 8)
    timeline = planner.estimate_timeline(project_id, team_size=3)
    
    architect = ArchitectureDesigner()
    architect.add_component("API Gateway", "gateway", [])
    architect.add_component("User Service", "service", ["API Gateway"])
    design = architect.design_architecture(ArchitecturePattern.MICROSERVICES)
    
    tech = TechStackRecommender()
    stack = tech.recommend_stack("web_application", "medium")
    
    risk = RiskAssessor()
    risks = risk.assess_risks({"name": "Test"})
    risk_summary = risk.get_risk_summary()
    
    sprint = SprintPlanner()
    stories = [
        {"id": 1, "title": "User login", "complexity": "medium"},
        {"id": 2, "title": "Product catalog", "complexity": "large"},
        {"id": 3, "title": "Shopping cart", "complexity": "medium"}
    ]
    stories = sprint.assign_story_points(stories)
    sprint_plan = sprint.create_sprint(1, stories, 2)
    
    print(f"Project: {project_id}")
    print(f"Timeline: {timeline['optimized_weeks']} weeks")
    print(f"Architecture: {design['pattern']}")
    print(f"Backend: {stack['stack']['backend'][0]}")
    print(f"High priority risks: {risk_summary['high_priority']}")
    print(f"Sprint points: {sprint_plan['total_points']}")

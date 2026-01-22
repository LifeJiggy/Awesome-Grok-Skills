"""
HR Agent
Human resources automation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class EmployeeStatus(Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    ONBOARDING = "onboarding"


class PerformanceRating(Enum):
    EXCEEDS = "exceeds"
    MEETS = "meets"
    DEVELOPING = "developing"
    NEEDS_IMPROVEMENT = "needs_improvement"


class EmployeeManager:
    """Employee management"""
    
    def __init__(self):
        self.employees = {}
        self.positions = {}
    
    def hire_employee(self, name: str, position: str, 
                     department: str, start_date: datetime, salary: float) -> Dict:
        """Hire new employee"""
        employee_id = f"EMP_{len(self.employees) + 1}"
        
        self.employees[employee_id] = {
            "id": employee_id,
            "name": name,
            "position": position,
            "department": department,
            "start_date": start_date,
            "salary": salary,
            "status": EmployeeStatus.ONBOARDING,
            "manager_id": None,
            "skills": [],
            "performance_history": [],
            "created_at": datetime.now()
        }
        
        return self.employees[employee_id]
    
    def update_status(self, employee_id: str, status: EmployeeStatus) -> bool:
        """Update employee status"""
        if employee_id not in self.employees:
            return False
        
        self.employees[employee_id]["status"] = status
        return True
    
    def assign_manager(self, employee_id: str, manager_id: str) -> bool:
        """Assign manager to employee"""
        if employee_id not in self.employees or manager_id not in self.employees:
            return False
        
        self.employees[employee_id]["manager_id"] = manager_id
        return True
    
    def get_organization_chart(self) -> Dict:
        """Get organization chart"""
        org_chart = {}
        
        for emp_id, emp in self.employees.items():
            manager_id = emp["manager_id"]
            if manager_id:
                if manager_id not in org_chart:
                    org_chart[manager_id] = []
                org_chart[manager_id].append(emp_id)
        
        return org_chart


class PayrollManager:
    """Payroll processing"""
    
    def __init__(self):
        self.payrolls = []
        self.payslips = {}
    
    def calculate_payroll(self, employee_id: str, month: int, year: int) -> Dict:
        """Calculate monthly payroll"""
        if employee_id not in self.employees:
            return {"error": "Employee not found"}
        
        employee = self.employees[employee_id]
        base_salary = employee["salary"]
        
        deductions = {
            "tax": base_salary * 0.22,
            "insurance": base_salary * 0.05,
            "pension": base_salary * 0.06
        }
        
        net_pay = base_salary - sum(deductions.values())
        
        payslip = {
            "employee_id": employee_id,
            "period": f"{year}-{month:02d}",
            "base_salary": base_salary,
            "gross_pay": base_salary,
            "deductions": deductions,
            "net_pay": net_pay,
            "processed_at": datetime.now()
        }
        
        self.payslips[f"{employee_id}:{year}-{month:02d}"] = payslip
        return payslip
    
    def process_bulk_payroll(self, month: int, year: int) -> Dict:
        """Process payroll for all employees"""
        results = {"processed": 0, "total_amount": 0, "failed": 0}
        
        for emp_id in self.employees:
            if self.employees[emp_id]["status"] == EmployeeStatus.ACTIVE:
                payroll = self.calculate_payroll(emp_id, month, year)
                if "error" not in payroll:
                    results["processed"] += 1
                    results["total_amount"] += payroll["net_pay"]
                else:
                    results["failed"] += 1
        
        self.payrolls.append({
            "month": month,
            "year": year,
            "results": results,
            "processed_at": datetime.now()
        })
        
        return results


class PerformanceManager:
    """Performance management"""
    
    def __init__(self):
        self.reviews = {}
        self.goals = {}
    
    def create_review(self, employee_id: str, reviewer_id: str,
                    period: str, rating: PerformanceRating, 
                    feedback: str) -> Dict:
        """Create performance review"""
        review_id = f"REV_{len(self.reviews) + 1}"
        
        self.reviews[review_id] = {
            "id": review_id,
            "employee_id": employee_id,
            "reviewer_id": reviewer_id,
            "period": period,
            "rating": rating.value,
            "feedback": feedback,
            "created_at": datetime.now()
        }
        
        self.employees[employee_id]["performance_history"].append(review_id)
        
        return self.reviews[review_id]
    
    def set_goal(self, employee_id: str, title: str, 
                description: str, due_date: datetime) -> Dict:
        """Set employee goal"""
        goal_id = f"GOAL_{len(self.goals) + 1}"
        
        self.goals[goal_id] = {
            "id": goal_id,
            "employee_id": employee_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "status": "active",
            "progress": 0,
            "created_at": datetime.now()
        }
        
        return self.goals[goal_id]
    
    def update_goal_progress(self, goal_id: str, progress: int) -> Dict:
        """Update goal progress"""
        if goal_id not in self.goals:
            return {"error": "Goal not found"}
        
        self.goals[goal_id]["progress"] = min(100, max(0, progress))
        if progress >= 100:
            self.goals[goal_id]["status"] = "completed"
            self.goals[goal_id]["completed_at"] = datetime.now()
        
        return self.goals[goal_id]
    
    def get_performance_summary(self, employee_id: str) -> Dict:
        """Get employee performance summary"""
        reviews = [self.reviews[r] for r in self.employees[employee_id]["performance_history"] 
                   if r in self.reviews]
        
        avg_rating = sum({
            "exceeds": 4, "meets": 3, "developing": 2, "needs_improvement": 1
        }.get(r["rating"], 0) for r in reviews) / max(len(reviews), 1)
        
        active_goals = [g for g in self.goals.values() 
                      if g["employee_id"] == employee_id and g["status"] == "active"]
        
        return {
            "employee_id": employee_id,
            "total_reviews": len(reviews),
            "average_rating": avg_rating,
            "active_goals": len(active_goals),
            "completed_goals": len([g for g in self.goals.values() 
                                  if g["employee_id"] == employee_id and g["status"] == "completed"])
        }


class RecruitmentManager:
    """Recruitment and hiring"""
    
    def __init__(self):
        self.jobs = {}
        self.applications = {}
    
    def post_job(self, title: str, department: str, 
                requirements: List[str], salary_range: tuple) -> str:
        """Post new job opening"""
        job_id = f"JOB_{len(self.jobs) + 1}"
        
        self.jobs[job_id] = {
            "id": job_id,
            "title": title,
            "department": department,
            "requirements": requirements,
            "salary_min": salary_range[0],
            "salary_max": salary_range[1],
            "status": "open",
            "applications": [],
            "posted_at": datetime.now()
        }
        
        return job_id
    
    def submit_application(self, job_id: str, candidate_name: str,
                         resume_url: str, cover_letter: str = None) -> Dict:
        """Submit job application"""
        if job_id not in self.jobs:
            return {"error": "Job not found"}
        
        application_id = f"APP_{len(self.applications) + 1}"
        
        self.applications[application_id] = {
            "id": application_id,
            "job_id": job_id,
            "candidate_name": candidate_name,
            "resume_url": resume_url,
            "cover_letter": cover_letter,
            "status": "submitted",
            "stage": "initial_review",
            "applied_at": datetime.now()
        }
        
        self.jobs[job_id]["applications"].append(application_id)
        
        return self.applications[application_id]
    
    def update_application_status(self, application_id: str, 
                                new_status: str, new_stage: str) -> Dict:
        """Update application status"""
        if application_id not in self.applications:
            return {"error": "Application not found"}
        
        self.applications[application_id]["status"] = new_status
        self.applications[application_id]["stage"] = new_stage
        
        return self.applications[application_id]
    
    def get_pipeline_report(self, job_id: str) -> Dict:
        """Get hiring pipeline report"""
        if job_id not in self.jobs:
            return {"error": "Job not found"}
        
        applications = self.applications.values()
        by_stage = {}
        
        for app in applications:
            if app["job_id"] == job_id:
                stage = app["stage"]
                by_stage[stage] = by_stage.get(stage, 0) + 1
        
        return {
            "job_id": job_id,
            "total_applications": len(self.jobs[job_id]["applications"]),
            "by_stage": by_stage
        }


class LeaveManager:
    """Leave management"""
    
    def __init__(self):
        self.leave_requests = {}
        self.leave_balances = {}
    
    def request_leave(self, employee_id: str, leave_type: str,
                     start_date: datetime, end_date: datetime, reason: str = None) -> Dict:
        """Submit leave request"""
        request_id = f"LR_{len(self.leave_requests) + 1}"
        
        days = (end_date - start_date).days + 1
        
        self.leave_requests[request_id] = {
            "id": request_id,
            "employee_id": employee_id,
            "type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "reason": reason,
            "status": "pending",
            "requested_at": datetime.now()
        }
        
        return self.leave_requests[request_id]
    
    def approve_leave(self, request_id: str, approver_id: str) -> Dict:
        """Approve leave request"""
        if request_id not in self.leave_requests:
            return {"error": "Request not found"}
        
        self.leave_requests[request_id]["status"] = "approved"
        self.leave_requests[request_id]["approver_id"] = approver_id
        self.leave_requests[request_id]["approved_at"] = datetime.now()
        
        return self.leave_requests[request_id]
    
    def get_leave_balance(self, employee_id: str, year: int) -> Dict:
        """Get employee leave balance"""
        annual_allowance = 20
        used = len([r for r in self.leave_requests.values() 
                  if r["employee_id"] == employee_id 
                  and r["start_date"].year == year 
                  and r["status"] == "approved"])
        
        return {
            "employee_id": employee_id,
            "year": year,
            "annual_allowance": annual_allowance,
            "used": used,
            "remaining": annual_allowance - used
        }


if __name__ == "__main__":
    employees = EmployeeManager()
    emp1 = employees.hire_employee("Alice Smith", "Engineer", "Engineering", datetime.now(), 80000)
    emp2 = employees.hire_employee("Bob Jones", "Manager", "Engineering", datetime.now(), 100000)
    employees.assign_manager(emp1["id"], emp2["id"])
    
    payroll = PayrollManager()
    payslip = payroll.calculate_payroll(emp1["id"], 1, 2024)
    
    performance = PerformanceManager()
    review = performance.create_review(emp1["id"], emp2["id"], "2024 Q1", 
                                     PerformanceRating.MEETS, "Good performance")
    goal = performance.set_goal(emp1["id"], "Learn Python", "Complete Python certification", 
                               datetime.now() + timedelta(days=90))
    perf_summary = performance.get_performance_summary(emp1["id"])
    
    recruitment = RecruitmentManager()
    job_id = recruitment.post_job("Senior Engineer", "Engineering", 
                                ["Python", "5 years exp"], (120000, 150000))
    application = recruitment.submit_application(job_id, "Charlie Brown", "/resumes/charlie.pdf")
    pipeline = recruitment.get_pipeline_report(job_id)
    
    leave = LeaveManager()
    leave_req = leave.request_leave(emp1["id"], "Annual", 
                                   datetime.now(), datetime.now() + timedelta(days=5), "Vacation")
    leave.approve_leave(leave_req["id"], emp2["id"])
    balance = leave.get_leave_balance(emp1["id"], 2024)
    
    print(f"Employee: {emp1['name']}")
    print(f"Net pay: ${payslip['net_pay']:.2f}")
    print(f"Performance rating: {perf_summary['average_rating']:.2f}")
    print(f"Job applications: {pipeline['total_applications']}")
    print(f"Leave balance: {balance['remaining']} days")

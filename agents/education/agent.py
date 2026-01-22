"""
Education Agent
Learning management and educational content
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class LearnerProgress(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class CourseManager:
    """Course creation and management"""
    
    def __init__(self):
        self.courses = {}
        self.modules = {}
        self.lessons = {}
    
    def create_course(self, title: str, description: str, instructor: str) -> str:
        """Create new course"""
        course_id = f"course_{len(self.courses) + 1}"
        
        self.courses[course_id] = {
            "id": course_id,
            "title": title,
            "description": description,
            "instructor": instructor,
            "status": CourseStatus.DRAFT,
            "modules": [],
            "enrollments": 0,
            "rating": 0,
            "created_at": datetime.now()
        }
        
        return course_id
    
    def add_module(self, course_id: str, title: str, order: int) -> str:
        """Add module to course"""
        module_id = f"module_{len(self.modules) + 1}"
        
        self.modules[module_id] = {
            "id": module_id,
            "course_id": course_id,
            "title": title,
            "order": order,
            "lessons": []
        }
        
        if course_id in self.courses:
            self.courses[course_id]["modules"].append(module_id)
        
        return module_id
    
    def add_lesson(self, module_id: str, title: str, content: str, 
                  lesson_type: str = "video", duration_minutes: int = 10) -> str:
        """Add lesson to module"""
        lesson_id = f"lesson_{len(self.lessons) + 1}"
        
        self.lessons[lesson_id] = {
            "id": lesson_id,
            "module_id": module_id,
            "title": title,
            "content": content,
            "type": lesson_type,
            "duration_minutes": duration_minutes,
            "resources": []
        }
        
        if module_id in self.modules:
            self.modules[module_id]["lessons"].append(lesson_id)
        
        return lesson_id
    
    def publish_course(self, course_id: str) -> bool:
        """Publish course"""
        if course_id in self.courses:
            self.courses[course_id]["status"] = CourseStatus.PUBLISHED
            return True
        return False
    
    def get_course_details(self, course_id: str) -> Dict:
        """Get course with all content"""
        if course_id not in self.courses:
            return {"error": "Course not found"}
        
        course = self.courses[course_id].copy()
        course["module_details"] = []
        
        for module_id in course["modules"]:
            if module_id in self.modules:
                module = self.modules[module_id].copy()
                module["lesson_details"] = [
                    self.lessons[lid] for lid in module["lessons"] if lid in self.lessons
                ]
                course["module_details"].append(module)
        
        return course


class LearnerManager:
    """Learner progress tracking"""
    
    def __init__(self):
        self.enrollments = {}
        self.progress = {}
    
    def enroll_learner(self, course_id: str, learner_id: str) -> str:
        """Enroll learner in course"""
        enrollment_id = f"enroll_{len(self.enrollments) + 1}"
        
        self.enrollments[enrollment_id] = {
            "id": enrollment_id,
            "course_id": course_id,
            "learner_id": learner_id,
            "status": LearnerProgress.NOT_STARTED,
            "progress_percent": 0,
            "started_at": None,
            "completed_at": None,
            "enrolled_at": datetime.now()
        }
        
        return enrollment_id
    
    def update_progress(self, enrollment_id: str, lesson_id: str, completed: bool = True) -> Dict:
        """Update lesson progress"""
        if enrollment_id not in self.enrollments:
            return {"error": "Enrollment not found"}
        
        enrollment = self.enrollments[enrollment_id]
        
        if enrollment["status"] == LearnerProgress.NOT_STARTED:
            enrollment["status"] = LearnerProgress.IN_PROGRESS
            enrollment["started_at"] = datetime.now()
        
        progress_key = f"{enrollment_id}:{lesson_id}"
        self.progress[progress_key] = {
            "completed": completed,
            "completed_at": datetime.now() if completed else None
        }
        
        enrollment["progress_percent"] = self._calculate_progress(enrollment_id)
        
        if enrollment["progress_percent"] >= 100:
            enrollment["status"] = LearnerProgress.COMPLETED
            enrollment["completed_at"] = datetime.now()
        
        return enrollment
    
    def _calculate_progress(self, enrollment_id: str) -> int:
        """Calculate progress percentage"""
        completed = len([k for k in self.progress.keys() 
                       if k.startswith(enrollment_id) and self.progress[k]["completed"]])
        total = len([k for k in self.progress.keys() if k.startswith(enrollment_id)])
        return int(completed / total * 100) if total > 0 else 0
    
    def get_learner_dashboard(self, learner_id: str) -> Dict:
        """Get learner dashboard"""
        enrollments = [e for e in self.enrollments.values() if e["learner_id"] == learner_id]
        
        return {
            "enrolled_courses": len(enrollments),
            "in_progress": len([e for e in enrollments if e["status"] == LearnerProgress.IN_PROGRESS]),
            "completed": len([e for e in enrollments if e["status"] == LearnerProgress.COMPLETED]),
            "courses": enrollments
        }


class QuizManager:
    """Quiz and assessment management"""
    
    def __init__(self):
        self.quizzes = {}
        self.responses = {}
    
    def create_quiz(self, title: str, course_id: str, passing_score: int = 70) -> str:
        """Create quiz"""
        quiz_id = f"quiz_{len(self.quizzes) + 1}"
        
        self.quizzes[quiz_id] = {
            "id": quiz_id,
            "title": title,
            "course_id": course_id,
            "questions": [],
            "passing_score": passing_score,
            "time_limit_minutes": 30
        }
        
        return quiz_id
    
    def add_question(self, quiz_id: str, question: str, options: List[str], 
                    correct_index: int, points: int = 1) -> str:
        """Add question to quiz"""
        question_id = f"q_{len(self.quizzes[quiz_id]['questions']) + 1}"
        
        self.quizzes[quiz_id]["questions"].append({
            "id": question_id,
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "points": points
        })
        
        return question_id
    
    def grade_quiz(self, quiz_id: str, answers: Dict[str, int]) -> Dict:
        """Grade quiz submission"""
        if quiz_id not in self.quizzes:
            return {"error": "Quiz not found"}
        
        quiz = self.quizzes[quiz_id]
        total_points = sum(q["points"] for q in quiz["questions"])
        earned_points = 0
        
        for question in quiz["questions"]:
            if answers.get(question["id"]) == question["correct_index"]:
                earned_points += question["points"]
        
        score_percent = (earned_points / total_points * 100) if total_points > 0 else 0
        
        return {
            "quiz_id": quiz_id,
            "score": earned_points,
            "total_points": total_points,
            "percentage": round(score_percent, 1),
            "passed": score_percent >= quiz["passing_score"],
            "passing_score": quiz["passing_score"]
        }


class CertificationManager:
    """Certificate generation"""
    
    def __init__(self):
        self.certificates = {}
    
    def issue_certificate(self, learner_id: str, course_id: str, 
                         completion_date: datetime) -> Dict:
        """Issue completion certificate"""
        cert_id = f"cert_{len(self.certificates) + 1}"
        
        certificate = {
            "id": cert_id,
            "learner_id": learner_id,
            "course_id": course_id,
            "issued_at": datetime.now(),
            "completion_date": completion_date,
            "certificate_number": f"CN-{datetime.now().strftime('%Y%m%d')}-{cert_id[-4:]}"
        }
        
        self.certificates[cert_id] = certificate
        return certificate
    
    def verify_certificate(self, certificate_number: str) -> Dict:
        """Verify certificate"""
        for cert in self.certificates.values():
            if cert["certificate_number"] == certificate_number:
                return {
                    "valid": True,
                    "learner_id": cert["learner_id"],
                    "course_id": cert["course_id"],
                    "issued_at": cert["issued_at"]
                }
        return {"valid": False}


class AnalyticsReporting:
    """Educational analytics"""
    
    def __init__(self):
        self.metrics = {}
    
    def get_course_analytics(self, course_id: str) -> Dict:
        """Get course analytics"""
        return {
            "course_id": course_id,
            "total_enrollments": 100,
            "active_learners": 75,
            "completion_rate": 60.0,
            "average_rating": 4.5,
            "avg_time_to_complete_hours": 20,
            "drop_off_points": ["Module 3", "Lesson 7"]
        }
    
    def get_engagement_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get engagement report"""
        return {
            "period": {"start": start_date, "end": end_date},
            "total_logins": 5000,
            "avg_session_duration_minutes": 25,
            "lessons_completed": 1200,
            "quizzes_taken": 800,
            "certificates_issued": 150
        }


if __name__ == "__main__":
    courses = CourseManager()
    course_id = courses.create_course("Python Basics", "Learn Python", "Dr. Smith")
    module_id = courses.add_module(course_id, "Getting Started", 1)
    lesson_id = courses.add_lesson(module_id, "Introduction", "Welcome to Python...", "video", 15)
    courses.publish_course(course_id)
    
    learners = LearnerManager()
    enrollment_id = learners.enroll_learner(course_id, "learner_001")
    learners.update_progress(enrollment_id, lesson_id, True)
    dashboard = learners.get_learner_dashboard("learner_001")
    
    quizzes = QuizManager()
    quiz_id = quizzes.create_quiz("Python Basics Quiz", course_id)
    quizzes.add_question(quiz_id, "What is Python?", ["Language", "Snake", "Game"], 0, 10)
    grade = quizzes.grade_quiz(quiz_id, {"1": 0})
    
    certs = CertificationManager()
    certificate = certs.issue_certificate("learner_001", course_id, datetime.now())
    verified = certs.verify_certificate(certificate["certificate_number"])
    
    analytics = AnalyticsReporting()
    course_stats = analytics.get_course_analytics(course_id)
    engagement = analytics.get_engagement_report(datetime.now() - timedelta(days=30), datetime.now())
    
    print(f"Course: {course_id}")
    print(f"Lessons: {lesson_id}")
    print(f"Enrollment: {enrollment_id}")
    print(f"Quiz grade: {grade['percentage']}%")
    print(f"Certificate: {certificate['certificate_number']}")
    print(f"Course completion rate: {course_stats['completion_rate']}%")

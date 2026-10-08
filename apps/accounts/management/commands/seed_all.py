from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile, StudentSkill, StudentInterest, StudentCareerGoal
from apps.skills.models import Skill, Interest
from apps.careers.models import Career
from apps.academics.models import College, Branch, Regulation
from apps.recommendations.engine.recommender import HybridRecommender

User = get_user_model()

class Command(BaseCommand):
    help = "Master Seeding Script for IntelliCourse AI. Runs all domain seeders and creates sample student & admin accounts."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Master Database Seed Engine..."))

        # 1. Run individual domain seeders
        call_command('seed_academics')
        call_command('seed_skills')
        call_command('seed_careers')
        call_command('seed_courses')
        call_command('seed_assessments')

        # 2. Create Admin Superuser
        admin_email = "admin@intellicourse.ai"
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                username="admin",
                first_name="IntelliCourse",
                last_name="Administrator",
                role=User.Role.ADMIN,
                password="AdminPassword123!"
            )
            self.stdout.write(self.style.SUCCESS(f"Created Admin account: {admin_email} (Password: AdminPassword123!)"))

        # 3. Create Sample Student Account with Onboarding Completed
        student_email = "student@intellicourse.ai"
        student_user, s_created = User.objects.get_or_create(
            email=student_email,
            defaults={
                "username": "demo_student",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "role": User.Role.STUDENT
            }
        )
        if s_created:
            student_user.set_password("StudentPassword123!")
            student_user.save()

        profile, _ = StudentProfile.objects.get_or_create(user=student_user)
        
        # Populate Profile Info
        cbit = College.objects.filter(code="CBIT").first()
        cse = Branch.objects.filter(code="CSE").first()
        r20 = Regulation.objects.filter(name="R20").first()

        profile.college = cbit
        profile.branch = cse
        profile.regulation = r20
        profile.current_semester = 4
        profile.cgpa = 8.65
        profile.weekly_learning_hours = 14
        profile.onboarding_completed = True
        profile.save()

        # Add Skills
        py_skill = Skill.objects.filter(name="Python").first()
        ds_skill = Skill.objects.filter(name="Data Structures").first()
        if py_skill:
            StudentSkill.objects.get_or_create(student=profile, skill=py_skill, defaults={"proficiency": 3, "confidence": 0.80})
        if ds_skill:
            StudentSkill.objects.get_or_create(student=profile, skill=ds_skill, defaults={"proficiency": 2, "confidence": 0.70})

        # Add Career Goal
        ai_career = Career.objects.filter(slug="ai-ml-engineer").first()
        if ai_career:
            StudentCareerGoal.objects.get_or_create(student=profile, career=ai_career, defaults={"is_primary": True, "target_semester": 8})

        # Add Interests
        ai_interest = Interest.objects.filter(name="Artificial Intelligence & Data Science").first()
        if ai_interest:
            StudentInterest.objects.get_or_create(student=profile, interest=ai_interest)

        # Generate initial recommendations for sample student
        HybridRecommender.generate_recommendations(profile, top_n=5, refresh=True)

        self.stdout.write(self.style.SUCCESS("Master Database Seeding Complete! Demo accounts ready."))

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.accounts.models import User
from apps.students.models import StudentProfile, StudentCareerGoal
from apps.academics.models import Branch
from apps.careers.models import Career

def create_custom_account(email="user@intellicourse.ai", password="UserPassword123!", first_name="AP", last_name="Student", branch_code="CSE", semester=5, career_search="Embedded"):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': User.Role.STUDENT,
            'is_verified': True
        }
    )
    user.set_password(password)
    user.save()

    profile, _ = StudentProfile.objects.get_or_create(user=user)
    branch = Branch.objects.filter(code=branch_code).first() or Branch.objects.first()
    profile.branch = branch
    profile.current_semester = semester
    profile.onboarding_completed = True
    profile.save()

    career = Career.objects.filter(name__icontains=career_search).first() or Career.objects.first()
    if career:
        StudentCareerGoal.objects.update_or_create(
            student=profile,
            career=career,
            defaults={'is_primary': True, 'priority': 1}
        )

    print(f"ACCOUNT_SUCCESS|{user.email}|{password}|{first_name} {last_name}|{branch.name if branch else 'CSE'}|Sem {semester}|{career.name if career else 'General'}")

if __name__ == "__main__":
    create_custom_account()

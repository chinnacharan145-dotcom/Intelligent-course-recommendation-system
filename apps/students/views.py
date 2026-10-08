from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import StudentProfile, StudentSkill, StudentInterest, StudentCareerGoal
from .serializers import (
    StudentProfileSerializer, StudentSkillSerializer,
    StudentInterestSerializer, StudentCareerGoalSerializer
)
from apps.skills.models import Skill, Interest
from apps.careers.models import Career, CareerSkill, CareerReadinessSnapshot, SkillGapSnapshot
from apps.academics.models import College, Branch, Regulation

class StudentProfileMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_or_create_profile(self, user):
        profile, created = StudentProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self.get_or_create_profile(request.user)
        serializer = StudentProfileSerializer(profile)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    def patch(self, request):
        profile = self.get_or_create_profile(request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Student profile updated successfully."
        })

    def put(self, request):
        return self.patch(request)


class OnboardingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        data = request.data

        # 1. Academic Info
        academic = data.get('academic', {})
        if 'college_id' in academic:
            profile.college_id = academic.get('college_id')
        if 'branch_id' in academic:
            profile.branch_id = academic.get('branch_id')
        if 'regulation_id' in academic:
            profile.regulation_id = academic.get('regulation_id')
        if 'current_semester' in academic:
            profile.current_semester = academic.get('current_semester')
        if 'cgpa' in academic:
            profile.cgpa = academic.get('cgpa')
        if 'weekly_learning_hours' in academic:
            profile.weekly_learning_hours = academic.get('weekly_learning_hours')

        # 2. Skills
        skills_input = data.get('skills', [])
        for item in skills_input:
            skill_id = item.get('skill_id')
            prof = item.get('proficiency', 1)
            if skill_id:
                skill_obj = get_object_or_404(Skill, id=skill_id)
                StudentSkill.objects.update_or_create(
                    student=profile,
                    skill=skill_obj,
                    defaults={'proficiency': prof, 'source': StudentSkill.SourceChoice.SELF_ASSESSMENT}
                )

        # 3. Career Goal
        career_input = data.get('career', {})
        career_id = career_input.get('career_id')
        if career_id:
            career_obj = get_object_or_404(Career, id=career_id)
            profile.career_goals.filter(is_primary=True).update(is_primary=False)
            StudentCareerGoal.objects.update_or_create(
                student=profile,
                career=career_obj,
                defaults={
                    'is_primary': True,
                    'target_semester': career_input.get('target_semester', 8)
                }
            )

        # 4. Interests
        interest_ids = data.get('interests', [])
        for i_id in interest_ids:
            interest_obj = get_object_or_404(Interest, id=i_id)
            StudentInterest.objects.get_or_create(
                student=profile,
                interest=interest_obj
            )

        profile.onboarding_completed = True
        profile.save()

        return Response({
            "success": True,
            "data": StudentProfileSerializer(profile).data,
            "message": "Onboarding completed successfully!"
        }, status=status.HTTP_200_OK)


class StudentSkillsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        skills = profile.skills.all()
        serializer = StudentSkillSerializer(skills, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        skill_id = request.data.get('skill_id')
        proficiency = request.data.get('proficiency', 1)
        source = request.data.get('source', StudentSkill.SourceChoice.SELF_ASSESSMENT)

        if not skill_id:
            return Response({"success": False, "message": "skill_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        skill_obj = get_object_or_404(Skill, id=skill_id)
        student_skill, created = StudentSkill.objects.update_or_create(
            student=profile,
            skill=skill_obj,
            defaults={'proficiency': proficiency, 'source': source}
        )

        return Response({
            "success": True,
            "data": StudentSkillSerializer(student_skill).data,
            "message": "Student skill updated successfully."
        })


class StudentSkillDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        student_skill = get_object_or_404(StudentSkill, pk=pk, student=profile)
        student_skill.delete()
        return Response({
            "success": True,
            "message": "Skill removed from profile."
        })


class StudentInterestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        interests = profile.interests.all()
        serializer = StudentInterestSerializer(interests, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        interest_ids = request.data.get('interest_ids', [])
        priority = request.data.get('priority', StudentInterest.Priority.HIGH)

        if isinstance(interest_ids, (int, str)):
            interest_ids = [interest_ids]

        for i_id in interest_ids:
            interest_obj = get_object_or_404(Interest, id=i_id)
            StudentInterest.objects.update_or_create(
                student=profile,
                interest=interest_obj,
                defaults={'priority': priority}
            )

        updated_interests = profile.interests.all()
        return Response({
            "success": True,
            "data": StudentInterestSerializer(updated_interests, many=True).data,
            "message": "Student interests updated."
        })


class StudentCareerGoalsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        goals = profile.career_goals.all()
        serializer = StudentCareerGoalSerializer(goals, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        career_id = request.data.get('career_id')
        is_primary = request.data.get('is_primary', True)

        if not career_id:
            return Response({"success": False, "message": "career_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        career_obj = get_object_or_404(Career, id=career_id)

        if is_primary:
            profile.career_goals.filter(is_primary=True).update(is_primary=False)

        goal, created = StudentCareerGoal.objects.update_or_create(
            student=profile,
            career=career_obj,
            defaults={'is_primary': is_primary}
        )

        return Response({
            "success": True,
            "data": StudentCareerGoalSerializer(goal).data,
            "message": "Career goal set successfully."
        })


class SkillGapsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        primary_goal = profile.career_goals.filter(is_primary=True).first()

        if not primary_goal:
            return Response({
                "success": True,
                "data": {"career": None, "gaps": []},
                "message": "No primary career goal selected."
            })

        career = primary_goal.career
        required_skills = CareerSkill.objects.filter(career=career).select_related('skill')

        student_skills_map = {
            ss.skill_id: ss.proficiency for ss in profile.skills.all()
        }

        gaps = []
        total_gap_sum = 0
        for req in required_skills:
            current_level = student_skills_map.get(req.skill_id, 0)
            gap_amount = max(0, req.required_level - current_level)
            if gap_amount > 0:
                total_gap_sum += gap_amount
                gaps.append({
                    "skill_id": str(req.skill.id),
                    "skill_name": req.skill.name,
                    "skill_category": req.skill.category.name if req.skill.category else None,
                    "current_level": current_level,
                    "required_level": req.required_level,
                    "gap": gap_amount,
                    "importance": req.importance,
                    "required": req.required
                })

        gaps.sort(key=lambda x: (x['gap'], x['importance']), reverse=True)

        avg_gap = round(total_gap_sum / len(gaps), 2) if gaps else 0.0
        SkillGapSnapshot.objects.create(
            student=profile,
            career=career,
            total_gaps_count=len(gaps),
            avg_gap_size=avg_gap
        )

        return Response({
            "success": True,
            "data": {
                "career_id": str(career.id),
                "career_name": career.name,
                "total_gaps_count": len(gaps),
                "average_gap_size": avg_gap,
                "gaps": gaps
            },
            "message": None
        })


class CareerReadinessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        primary_goal = profile.career_goals.filter(is_primary=True).first()

        if not primary_goal:
            return Response({
                "success": True,
                "data": {"readiness_percentage": 0, "career_name": "Not Selected", "analysis": "Select a career goal to calculate readiness."},
                "message": None
            })

        career = primary_goal.career
        required_skills = CareerSkill.objects.filter(career=career)

        if not required_skills.exists():
            return Response({
                "success": True,
                "data": {"readiness_percentage": 100, "career_name": career.name, "analysis": "No specific skill prerequisites defined for this career."},
                "message": None
            })

        student_skills_map = {
            ss.skill_id: ss.proficiency for ss in profile.skills.all()
        }

        total_weight = 0.0
        earned_weight = 0.0

        for req in required_skills:
            weight = req.importance * (2.0 if req.required else 1.0)
            total_weight += weight
            current = student_skills_map.get(req.skill_id, 0)
            ratio = min(1.0, current / req.required_level) if req.required_level > 0 else 1.0
            earned_weight += weight * ratio

        readiness_pct = round((earned_weight / total_weight) * 100, 1) if total_weight > 0 else 0.0

        # Create readiness snapshot record
        CareerReadinessSnapshot.objects.create(
            student=profile,
            career=career,
            readiness_score=readiness_pct
        )

        history_qs = CareerReadinessSnapshot.objects.filter(student=profile, career=career)[:10]
        history = [
            {
                "readiness_score": float(h.readiness_score),
                "calculated_at": h.calculated_at
            }
            for h in history_qs
        ]

        return Response({
            "success": True,
            "data": {
                "career_id": str(career.id),
                "career_name": career.name,
                "readiness_percentage": readiness_pct,
                "earned_points": round(earned_weight, 2),
                "total_points": round(total_weight, 2),
                "history": history
            },
            "message": None
        })

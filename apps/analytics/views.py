from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Avg
from apps.students.models import StudentProfile, StudentSkill, StudentInterest, StudentCareerGoal
from apps.learning.models import StudentCourse, LearningActivity
from apps.recommendations.models import Recommendation, RecommendationFeedback
from apps.recommendations.engine.recommender import HybridRecommender
from apps.recommendations.serializers import RecommendationSerializer
from apps.careers.models import CareerSkill
from apps.courses.models import Course, CourseProvider
from apps.academics.models import College, Branch

class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        # 1. Profile Completion Calculation
        fields_to_check = [
            profile.college_id, profile.branch_id, profile.regulation_id,
            profile.current_semester, profile.cgpa, profile.weekly_learning_hours
        ]
        filled = sum(1 for f in fields_to_check if f)
        has_skills = profile.skills.exists()
        has_interests = profile.interests.exists()
        has_career = profile.career_goals.exists()
        
        total_checks = len(fields_to_check) + 3
        actual_checks = filled + (1 if has_skills else 0) + (1 if has_interests else 0) + (1 if has_career else 0)
        profile_completion_pct = round((actual_checks / total_checks) * 100)

        # 2. Career Readiness Calculation
        primary_goal = profile.career_goals.filter(is_primary=True).first()
        readiness_pct = 0.0
        career_name = "Not Selected"
        gaps = []

        if primary_goal:
            career = primary_goal.career
            career_name = career.name
            req_skills = CareerSkill.objects.filter(career=career)
            student_skills_map = {ss.skill_id: ss.proficiency for ss in profile.skills.all()}

            total_weight = 0.0
            earned_weight = 0.0

            for req in req_skills:
                weight = req.importance * (2.0 if req.required else 1.0)
                total_weight += weight
                curr_lvl = student_skills_map.get(req.skill_id, 0)
                ratio = min(1.0, curr_lvl / req.required_level) if req.required_level > 0 else 1.0
                earned_weight += weight * ratio

                gap_amt = max(0, req.required_level - curr_lvl)
                if gap_amt > 0:
                    gaps.append({
                        "skill_id": str(req.skill.id),
                        "skill_name": req.skill.name,
                        "skill_category": req.skill.category.name if req.skill.category else None,
                        "current_level": curr_lvl,
                        "required_level": req.required_level,
                        "gap": gap_amt,
                        "importance": req.importance
                    })

            readiness_pct = round((earned_weight / total_weight) * 100, 1) if total_weight > 0 else 100.0
            gaps.sort(key=lambda x: (x['gap'], x['importance']), reverse=True)

        # 3. Learning Stats
        student_courses = profile.courses.all()
        in_progress_count = student_courses.filter(status=StudentCourse.Status.IN_PROGRESS).count()
        completed_count = student_courses.filter(status=StudentCourse.Status.COMPLETED).count()

        # 4. Top Recommendations
        recs = HybridRecommender.generate_recommendations(profile, top_n=5, refresh=False)
        recs_data = RecommendationSerializer(recs, many=True).data

        # 5. Recent Activity
        recent_activities = LearningActivity.objects.filter(student=profile).order_by('-timestamp')[:5]
        activity_data = [
            {
                "id": str(act.id),
                "activity_type": act.activity_type,
                "course_title": act.course.title if act.course else "General",
                "timestamp": act.timestamp
            }
            for act in recent_activities
        ]

        return Response({
            "success": True,
            "data": {
                "profile_completion": profile_completion_pct,
                "career_readiness": readiness_pct,
                "career_name": career_name,
                "skills_count": profile.skills.count(),
                "completed_courses_count": completed_count,
                "in_progress_courses_count": in_progress_count,
                "weekly_learning_hours": profile.weekly_learning_hours,
                "top_recommendations": recs_data,
                "skill_gaps": gaps[:4],
                "recent_activity": activity_data
            },
            "message": None
        })

class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_students = StudentProfile.objects.count()
        active_students = StudentProfile.objects.filter(onboarding_completed=True).count()
        total_courses = Course.objects.filter(is_active=True).count()
        total_colleges = College.objects.filter(is_active=True).count()
        total_recs = Recommendation.objects.count()

        # Feedback analytics
        feedbacks = RecommendationFeedback.objects.all()
        total_feedbacks = feedbacks.count()
        positive_feedbacks = feedbacks.filter(feedback_type='INTERESTED').count()
        acceptance_rate = round((positive_feedbacks / total_feedbacks * 100), 1) if total_feedbacks > 0 else 100.0

        # Branch distribution
        branch_dist = StudentProfile.objects.values('branch__name', 'branch__code').annotate(count=Count('id')).order_by('-count')

        # Popular Careers
        popular_careers = StudentCareerGoal.objects.values('career__name').annotate(count=Count('id')).order_by('-count')[:5]

        # Top Recommended Courses
        top_courses = Recommendation.objects.values('course__title').annotate(count=Count('id'), avg_score=Avg('match_score')).order_by('-count')[:5]

        return Response({
            "success": True,
            "data": {
                "total_students": total_students,
                "active_students": active_students,
                "total_courses": total_courses,
                "total_colleges": total_colleges,
                "total_recommendations": total_recs,
                "acceptance_rate": acceptance_rate,
                "branch_distribution": list(branch_dist),
                "popular_careers": list(popular_careers),
                "top_recommended_courses": list(top_courses)
            },
            "message": None
        })

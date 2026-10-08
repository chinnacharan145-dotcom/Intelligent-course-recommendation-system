from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Recommendation, RecommendationReason, RecommendationFeedback
from .serializers import RecommendationSerializer, RecommendationFeedbackSerializer
from .engine.recommender import HybridRecommender
from apps.students.models import StudentProfile
from apps.careers.models import CareerSkill

class RecommendationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        top_n = int(request.query_params.get('top_n', 10))
        refresh = request.query_params.get('refresh', 'false').lower() in ('true', '1')

        recs = HybridRecommender.generate_recommendations(profile, top_n=top_n, refresh=refresh)
        serializer = RecommendationSerializer(recs, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": f"Retrieved top {len(recs)} recommendations."
        })


class GenerateRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        top_n = int(request.data.get('limit', 10))
        refresh = request.data.get('refresh', True)

        recs = HybridRecommender.generate_recommendations(profile, top_n=top_n, refresh=refresh)
        serializer = RecommendationSerializer(recs, many=True)
        return Response({
            "success": True,
            "data": {
                "student_id": str(profile.id),
                "algorithm_version": HybridRecommender.ALGORITHM_VERSION,
                "recommendations": serializer.data
            },
            "message": "Recommendations successfully generated."
        })


class RecommendationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        rec = get_object_or_404(Recommendation, pk=pk, student__user=request.user)
        serializer = RecommendationSerializer(rec)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })


class RecommendationExplanationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        rec = get_object_or_404(Recommendation, pk=pk, student__user=request.user)
        reasons = [r.reason_text for r in rec.reasons.all()]
        return Response({
            "success": True,
            "data": {
                "course_id": str(rec.course.id),
                "course_title": rec.course.title,
                "match_score": float(rec.match_score),
                "reasons": reasons,
                "breakdown": {
                    "skill_match_score": float(rec.skill_match_score) if rec.skill_match_score else None,
                    "career_match_score": float(rec.career_match_score) if rec.career_match_score else None,
                    "branch_match_score": float(rec.branch_match_score) if rec.branch_match_score else None,
                    "difficulty_match_score": float(rec.difficulty_match_score) if rec.difficulty_match_score else None,
                    "content_similarity_score": float(rec.content_similarity_score) if rec.content_similarity_score else None,
                }
            },
            "message": None
        })


class RecommendationFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        rec = get_object_or_404(Recommendation, pk=pk, student__user=request.user)
        feedback_type = request.data.get('feedback_type', RecommendationFeedback.FeedbackType.INTERESTED)
        comments = request.data.get('comments', '')

        feedback = RecommendationFeedback.objects.create(
            recommendation=rec,
            student=rec.student,
            feedback_type=feedback_type,
            comments=comments
        )

        return Response({
            "success": True,
            "data": RecommendationFeedbackSerializer(feedback).data,
            "message": "Thank you for your feedback!"
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from apps.recommendations.models import Recommendation
from .services import GeminiAssistantService

class AIRecommendationExplanationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, rec_id=None):
        rec = get_object_or_404(Recommendation, pk=rec_id, student__user=request.user)
        ai_res = GeminiAssistantService.explain_recommendation_with_ai(rec)
        return Response({
            "success": True,
            "data": ai_res,
            "message": None
        })

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Assessment, AssessmentQuestion, AssessmentOption,
    AssessmentAttempt, StudentAnswer, AssessmentResult
)
from .serializers import (
    AssessmentSerializer, AssessmentDetailSerializer,
    AssessmentAttemptSerializer
)
from .scoring import calculate_assessment_score
from apps.students.models import StudentProfile

class AssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assessment.objects.filter(is_active=True).order_by('title')
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AssessmentDetailSerializer
        return AssessmentSerializer

class StartAssessmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        assessment = get_object_or_404(Assessment, pk=pk, is_active=True)
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        attempt = AssessmentAttempt.objects.create(
            student=profile,
            assessment=assessment
        )

        for q in assessment.questions.all():
            StudentAnswer.objects.create(
                attempt=attempt,
                question=q
            )

        serializer = AssessmentDetailSerializer(assessment)
        return Response({
            "success": True,
            "data": {
                "attempt_id": attempt.id,
                "assessment": serializer.data,
                "started_at": attempt.started_at
            },
            "message": "Assessment attempt started."
        })

class RecordAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, attempt_id=None):
        attempt = get_object_or_404(AssessmentAttempt, id=attempt_id, student__user=request.user)
        question_id = request.data.get('question_id')
        option_id = request.data.get('option_id')

        if not question_id or not option_id:
            return Response({"success": False, "message": "question_id and option_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(AssessmentQuestion, id=question_id, assessment=attempt.assessment)
        option = get_object_or_404(AssessmentOption, id=option_id, question=question)

        answer, created = StudentAnswer.objects.get_or_create(
            attempt=attempt,
            question=question
        )
        answer.selected_option = option
        answer.save()

        return Response({
            "success": True,
            "message": "Answer recorded.",
            "data": {"attempt_id": attempt.id, "question_id": question.id, "selected_option_id": option.id}
        })

class SubmitAssessmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, attempt_id=None):
        attempt = get_object_or_404(AssessmentAttempt, id=attempt_id, student__user=request.user)

        if attempt.submitted_at:
            return Response({
                "success": True,
                "data": AssessmentAttemptSerializer(attempt).data,
                "message": "Assessment was already submitted."
            })

        completed_attempt = calculate_assessment_score(attempt)
        serializer = AssessmentAttemptSerializer(completed_attempt)

        return Response({
            "success": True,
            "data": serializer.data,
            "message": f"Assessment completed! Your score: {completed_attempt.percentage}%."
        })

class AssessmentResultView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, attempt_id=None):
        attempt = get_object_or_404(AssessmentAttempt, id=attempt_id, student__user=request.user)
        serializer = AssessmentAttemptSerializer(attempt)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

class StudentAssessmentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        attempts = profile.assessment_attempts.all().order_by('-started_at')
        serializer = AssessmentAttemptSerializer(attempts, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

from rest_framework import serializers
from .models import Recommendation, RecommendationReason, RecommendationFeedback
from apps.courses.serializers import CourseSerializer

class RecommendationReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationReason
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    reasons = RecommendationReasonSerializer(many=True, read_only=True)

    class Meta:
        model = Recommendation
        fields = '__all__'

class RecommendationFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationFeedback
        fields = '__all__'
        read_only_fields = ['student', 'created_at']

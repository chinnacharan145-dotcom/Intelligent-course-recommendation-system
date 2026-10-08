from rest_framework import serializers
from .models import (
    Assessment, AssessmentQuestion, AssessmentOption,
    AssessmentAttempt, StudentAnswer, AssessmentResult, AssessmentSkillResult
)

class AssessmentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentOption
        fields = ['id', 'option_text', 'option_order']

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    options = AssessmentOptionSerializer(many=True, read_only=True)
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'skill', 'skill_name', 'question_text', 'question_type', 'marks', 'difficulty', 'question_order', 'options']

class AssessmentSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Assessment
        fields = '__all__'

class AssessmentDetailSerializer(serializers.ModelSerializer):
    questions = AssessmentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'

class AssessmentSkillResultSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = AssessmentSkillResult
        fields = '__all__'

class AssessmentResultSerializer(serializers.ModelSerializer):
    skill_results = AssessmentSkillResultSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentResult
        fields = '__all__'

class AssessmentAttemptSerializer(serializers.ModelSerializer):
    result = AssessmentResultSerializer(read_only=True)

    class Meta:
        model = AssessmentAttempt
        fields = '__all__'

from rest_framework import serializers
from .models import Career, CareerSkill, CareerReadinessSnapshot, SkillGapSnapshot
from apps.skills.serializers import SkillSerializer

class CareerSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = CareerSkill
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    required_skills = CareerSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Career
        fields = '__all__'

class CareerReadinessSnapshotSerializer(serializers.ModelSerializer):
    career_name = serializers.ReadOnlyField(source='career.name')

    class Meta:
        model = CareerReadinessSnapshot
        fields = '__all__'

class SkillGapSnapshotSerializer(serializers.ModelSerializer):
    career_name = serializers.ReadOnlyField(source='career.name')

    class Meta:
        model = SkillGapSnapshot
        fields = '__all__'

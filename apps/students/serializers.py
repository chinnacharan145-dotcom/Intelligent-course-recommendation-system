from rest_framework import serializers
from .models import StudentProfile, StudentSkill, StudentSkillHistory, StudentInterest, StudentCareerGoal
from apps.academics.serializers import CollegeSerializer, UniversitySerializer, BranchSerializer, RegulationSerializer
from apps.skills.serializers import SkillSerializer, InterestSerializer
from apps.careers.serializers import CareerSerializer

class StudentSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')
    skill_category = serializers.ReadOnlyField(source='skill.category.name')

    class Meta:
        model = StudentSkill
        fields = '__all__'

class StudentSkillHistorySerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = StudentSkillHistory
        fields = '__all__'

class StudentInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.ReadOnlyField(source='interest.name')

    class Meta:
        model = StudentInterest
        fields = '__all__'

class StudentCareerGoalSerializer(serializers.ModelSerializer):
    career_name = serializers.ReadOnlyField(source='career.name')

    class Meta:
        model = StudentCareerGoal
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    college_detail = CollegeSerializer(source='college', read_only=True)
    university_detail = UniversitySerializer(source='university', read_only=True)
    branch_detail = BranchSerializer(source='branch', read_only=True)
    regulation_detail = RegulationSerializer(source='regulation', read_only=True)
    skills = StudentSkillSerializer(many=True, read_only=True)
    interests = StudentInterestSerializer(many=True, read_only=True)
    career_goals = StudentCareerGoalSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

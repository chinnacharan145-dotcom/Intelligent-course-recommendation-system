from rest_framework import serializers
from .models import CourseProvider, CourseCategory, Course, CourseSkill, CoursePrerequisite
from apps.skills.serializers import SkillSerializer

class CourseProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProvider
        fields = '__all__'

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'

class CourseSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = CourseSkill
        fields = '__all__'

class CoursePrerequisiteSerializer(serializers.ModelSerializer):
    required_skill_name = serializers.ReadOnlyField(source='required_skill.name')

    class Meta:
        model = CoursePrerequisite
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source='provider.name')
    category_name = serializers.ReadOnlyField(source='category.name')
    skills = CourseSkillSerializer(many=True, read_only=True)
    prerequisites = CoursePrerequisiteSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

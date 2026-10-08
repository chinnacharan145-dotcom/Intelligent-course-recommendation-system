from rest_framework import serializers
from .models import SkillCategory, Skill, SkillPrerequisite, Interest

class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Skill
        fields = '__all__'

class SkillPrerequisiteSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')
    prerequisite_skill_name = serializers.ReadOnlyField(source='prerequisite_skill.name')

    class Meta:
        model = SkillPrerequisite
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

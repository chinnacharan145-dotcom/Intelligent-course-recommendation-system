from rest_framework import serializers
from .models import Roadmap, RoadmapNode, RoadmapNodeSkill, Action, StudentAction, StudentActionHistory
from apps.skills.serializers import SkillSerializer

class RoadmapNodeSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = RoadmapNodeSkill
        fields = '__all__'

class RoadmapNodeSerializer(serializers.ModelSerializer):
    node_skills = RoadmapNodeSkillSerializer(many=True, read_only=True)

    class Meta:
        model = RoadmapNode
        fields = '__all__'

class RoadmapSerializer(serializers.ModelSerializer):
    nodes = RoadmapNodeSerializer(many=True, read_only=True)
    career_name = serializers.ReadOnlyField(source='career.name')

    class Meta:
        model = Roadmap
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class StudentActionSerializer(serializers.ModelSerializer):
    action_details = ActionSerializer(source='action', read_only=True)

    class Meta:
        model = StudentAction
        fields = '__all__'

class StudentActionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentActionHistory
        fields = '__all__'

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SkillCategory, Skill, SkillPrerequisite, Interest
from .serializers import (
    SkillCategorySerializer, SkillSerializer,
    SkillPrerequisiteSerializer, InterestSerializer
)
from apps.accounts.permissions import IsAdminOrReadOnly
from .services import get_skill_prerequisite_dag, get_skill_dependents

class SkillCategoryViewSet(viewsets.ModelViewSet):
    queryset = SkillCategory.objects.all().order_by('name')
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.filter(is_active=True).select_related('category').order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        cat = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if cat:
            qs = qs.filter(category_id=cat)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    @action(detail=True, methods=['get'])
    def graph(self, request, pk=None):
        skill = self.get_object()
        prereq_tree = get_skill_prerequisite_dag(skill.id)
        dependents = get_skill_dependents(skill.id)
        return Response({
            "success": True,
            "data": {
                "skill": SkillSerializer(skill).data,
                "prerequisites_tree": prereq_tree,
                "dependents": dependents
            },
            "message": None
        })


class SkillPrerequisiteViewSet(viewsets.ModelViewSet):
    queryset = SkillPrerequisite.objects.all().select_related('skill', 'prerequisite_skill').order_by('skill__name')
    serializer_class = SkillPrerequisiteSerializer
    permission_classes = [IsAdminOrReadOnly]


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.filter(is_active=True).order_by('name')
    serializer_class = InterestSerializer
    permission_classes = [IsAdminOrReadOnly]

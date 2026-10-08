from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import CourseProvider, CourseCategory, Course, CourseSkill, CoursePrerequisite
from .serializers import (
    CourseProviderSerializer, CourseCategorySerializer,
    CourseSerializer, CourseSkillSerializer, CoursePrerequisiteSerializer
)
from apps.accounts.permissions import IsAdminOrReadOnly

class CourseProviderViewSet(viewsets.ModelViewSet):
    queryset = CourseProvider.objects.filter(is_active=True).order_by('name')
    serializer_class = CourseProviderSerializer
    permission_classes = [IsAdminOrReadOnly]

class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.filter(is_active=True).order_by('name')
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True).select_related('provider', 'category').prefetch_related('skills__skill', 'prerequisites__required_skill').order_by('-rating', 'title')
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        provider = self.request.query_params.get('provider')
        difficulty = self.request.query_params.get('difficulty')
        free_only = self.request.query_params.get('free')
        skill = self.request.query_params.get('skill')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category:
            qs = qs.filter(category_id=category)
        if provider:
            qs = qs.filter(provider_id=provider)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if free_only and free_only.lower() in ('true', '1'):
            qs = qs.filter(is_free=True)
        if skill:
            qs = qs.filter(skills__skill_id=skill)

        return qs.distinct()

    @action(detail=True, methods=['get'])
    def prerequisites(self, request, pk=None):
        course = self.get_object()
        prereqs = course.prerequisites.all()
        serializer = CoursePrerequisiteSerializer(prereqs, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        course = self.get_object()
        related_courses = Course.objects.filter(
            category=course.category, is_active=True
        ).exclude(id=course.id).order_by('-rating')[:5]
        serializer = CourseSerializer(related_courses, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": None
        })

class CourseSkillViewSet(viewsets.ModelViewSet):
    queryset = CourseSkill.objects.all().select_related('course', 'skill').order_by('course__title')
    serializer_class = CourseSkillSerializer
    permission_classes = [IsAdminOrReadOnly]

class CoursePrerequisiteViewSet(viewsets.ModelViewSet):
    queryset = CoursePrerequisite.objects.all().select_related('course', 'required_skill').order_by('course__title')
    serializer_class = CoursePrerequisiteSerializer
    permission_classes = [IsAdminOrReadOnly]

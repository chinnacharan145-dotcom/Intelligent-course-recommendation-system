from rest_framework import viewsets, permissions
from .models import Career, CareerSkill, CareerReadinessSnapshot, SkillGapSnapshot
from .serializers import (
    CareerSerializer, CareerSkillSerializer,
    CareerReadinessSnapshotSerializer, SkillGapSnapshotSerializer
)
from apps.accounts.permissions import IsAdminOrReadOnly

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.filter(is_active=True).prefetch_related('required_skills__skill').order_by('name')
    serializer_class = CareerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        industry = self.request.query_params.get('industry')
        if search:
            qs = qs.filter(name__icontains=search)
        if industry:
            qs = qs.filter(industry__icontains=industry)
        return qs


class CareerSkillViewSet(viewsets.ModelViewSet):
    queryset = CareerSkill.objects.all().select_related('career', 'skill').order_by('career__name')
    serializer_class = CareerSkillSerializer
    permission_classes = [IsAdminOrReadOnly]

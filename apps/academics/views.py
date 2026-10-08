from rest_framework import viewsets, permissions
from .models import University, College, Branch, Regulation, AcademicYear, Semester, Subject, BranchSubject
from .serializers import (
    UniversitySerializer, CollegeSerializer, BranchSerializer,
    RegulationSerializer, AcademicYearSerializer, SemesterSerializer,
    SubjectSerializer, BranchSubjectSerializer
)
from apps.accounts.permissions import IsAdminOrReadOnly

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.filter(is_active=True).order_by('name')
    serializer_class = UniversitySerializer
    permission_classes = [IsAdminOrReadOnly]

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.filter(is_active=True).order_by('name')
    serializer_class = CollegeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        university_id = self.request.query_params.get('university')
        if university_id:
            qs = qs.filter(university_id=university_id)
        return qs

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.filter(is_active=True).order_by('name')
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrReadOnly]

class RegulationViewSet(viewsets.ModelViewSet):
    queryset = Regulation.objects.filter(is_active=True).order_by('name')
    serializer_class = RegulationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        university_id = self.request.query_params.get('university')
        if university_id:
            qs = qs.filter(university_id=university_id)
        return qs

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.filter(is_active=True).order_by('name')
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAdminOrReadOnly]

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all().order_by('number')
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(is_active=True).order_by('code')
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]

class BranchSubjectViewSet(viewsets.ModelViewSet):
    queryset = BranchSubject.objects.all().select_related('branch', 'regulation', 'semester', 'subject').order_by('branch__name', 'semester__number', 'subject__code')
    serializer_class = BranchSubjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        branch = self.request.query_params.get('branch')
        regulation = self.request.query_params.get('regulation')
        semester = self.request.query_params.get('semester')
        if branch:
            qs = qs.filter(branch_id=branch)
        if regulation:
            qs = qs.filter(regulation_id=regulation)
        if semester:
            qs = qs.filter(semester_id=semester)
        return qs

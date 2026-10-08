from rest_framework import serializers
from .models import University, College, Branch, Regulation, AcademicYear, Semester, Subject, BranchSubject

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    university_name = serializers.ReadOnlyField(source='university.name')

    class Meta:
        model = College
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class RegulationSerializer(serializers.ModelSerializer):
    university_code = serializers.ReadOnlyField(source='university.code')

    class Meta:
        model = Regulation
        fields = '__all__'

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class BranchSubjectSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    branch_name = serializers.ReadOnlyField(source='branch.name')
    semester_number = serializers.ReadOnlyField(source='semester.number')

    class Meta:
        model = BranchSubject
        fields = '__all__'

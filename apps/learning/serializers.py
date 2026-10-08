from rest_framework import serializers
from .models import StudentCourse, LearningActivity
from apps.courses.serializers import CourseSerializer

class StudentCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = StudentCourse
        fields = '__all__'
        read_only_fields = ['student', 'started_at', 'created_at', 'updated_at']

class LearningActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningActivity
        fields = '__all__'
        read_only_fields = ['student', 'timestamp']

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import StudentCourse, LearningActivity
from .serializers import StudentCourseSerializer, LearningActivitySerializer
from apps.courses.models import Course, CourseSkill
from apps.students.models import StudentProfile, StudentSkill

class StartCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id=None):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        course = get_object_or_404(Course, id=course_id)

        student_course, created = StudentCourse.objects.get_or_create(
            student=profile,
            course=course,
            defaults={'status': StudentCourse.Status.IN_PROGRESS, 'progress': 5.0}
        )

        LearningActivity.objects.create(
            student=profile,
            course=course,
            activity_type='START',
            duration_minutes=0
        )

        return Response({
            "success": True,
            "data": StudentCourseSerializer(student_course).data,
            "message": "Course started!"
        })


class UpdateCourseProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk=None):
        student_course = get_object_or_404(StudentCourse, pk=pk, student__user=request.user)
        progress_val = request.data.get('progress')
        status_val = request.data.get('status')

        if progress_val is not None:
            student_course.progress = min(100.0, max(0.0, float(progress_val)))
        if status_val:
            student_course.status = status_val

        if student_course.progress >= 100.0 or student_course.status == StudentCourse.Status.COMPLETED:
            student_course.status = StudentCourse.Status.COMPLETED
            if not student_course.completed_at:
                student_course.completed_at = timezone.now()

        student_course.save()

        return Response({
            "success": True,
            "data": StudentCourseSerializer(student_course).data,
            "message": "Course progress updated."
        })


class CompleteCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id=None):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        course = get_object_or_404(Course, id=course_id)

        student_course, created = StudentCourse.objects.update_or_create(
            student=profile,
            course=course,
            defaults={
                'status': StudentCourse.Status.COMPLETED,
                'progress': 100.0,
                'completed_at': timezone.now()
            }
        )

        LearningActivity.objects.create(
            student=profile,
            course=course,
            activity_type='COMPLETE',
            duration_minutes=0
        )

        # Award skills taught in this course to student profile!
        taught_skills = course.skills.all()
        for cs in taught_skills:
            target_lvl = min(5, max(1, cs.level))
            current_ss = StudentSkill.objects.filter(student=profile, skill=cs.skill).first()
            if not current_ss or current_ss.proficiency < target_lvl:
                StudentSkill.objects.update_or_create(
                    student=profile,
                    skill=cs.skill,
                    defaults={
                        'proficiency': target_lvl,
                        'source': StudentSkill.SourceChoice.COURSE_COMPLETION,
                        'confidence': 0.90
                    }
                )

        return Response({
            "success": True,
            "data": StudentCourseSerializer(student_course).data,
            "message": "Congratulations on completing the course! Skills acquired have been updated on your profile."
        })


class StudentProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        student_courses = profile.courses.all().select_related('course', 'course__provider')
        in_progress = student_courses.filter(status=StudentCourse.Status.IN_PROGRESS)
        completed = student_courses.filter(status=StudentCourse.Status.COMPLETED)

        return Response({
            "success": True,
            "data": {
                "total_enrolled": student_courses.count(),
                "in_progress_count": in_progress.count(),
                "completed_count": completed.count(),
                "in_progress": StudentCourseSerializer(in_progress, many=True).data,
                "completed": StudentCourseSerializer(completed, many=True).data
            },
            "message": None
        })

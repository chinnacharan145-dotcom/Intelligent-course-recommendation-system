from apps.courses.models import Course
from apps.learning.models import StudentCourse

def get_candidate_courses(student_profile, base_qs=None):
    if base_qs is None:
        base_qs = Course.objects.filter(is_active=True)
    else:
        base_qs = base_qs.filter(is_active=True)

    completed_course_ids = StudentCourse.objects.filter(
        student=student_profile,
        status=StudentCourse.Status.COMPLETED
    ).values_list('course_id', flat=True)

    candidate_qs = base_qs.exclude(id__in=completed_course_ids).select_related(
        'provider', 'category'
    ).prefetch_related(
        'skills__skill',
        'prerequisites__required_skill'
    )

    return list(candidate_qs)

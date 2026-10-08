from django.utils import timezone
from .models import AssessmentAttempt, StudentAnswer, AssessmentOption, AssessmentResult, AssessmentSkillResult
from apps.students.models import StudentSkill, StudentSkillHistory

def calculate_assessment_score(attempt: AssessmentAttempt):
    answers = attempt.answers.all().select_related('question', 'selected_option')
    total_questions = answers.count()
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    total_possible_marks = float(sum(ans.question.marks for ans in answers))
    total_earned_marks = 0.0

    for ans in answers:
        if ans.selected_option is None:
            unanswered_count += 1
            ans.is_correct = False
            ans.marks_obtained = 0.0
        elif ans.selected_option.is_correct:
            correct_count += 1
            ans.is_correct = True
            ans.marks_obtained = float(ans.question.marks)
            total_earned_marks += float(ans.question.marks)
        else:
            incorrect_count += 1
            ans.is_correct = False
            ans.marks_obtained = 0.0
        ans.save()

    percentage = (total_earned_marks / total_possible_marks * 100.0) if total_possible_marks > 0 else 0.0

    # Map percentage to 1-5 proficiency level
    if percentage >= 90.0:
        new_proficiency = 5
    elif percentage >= 75.0:
        new_proficiency = 4
    elif percentage >= 60.0:
        new_proficiency = 3
    elif percentage >= 40.0:
        new_proficiency = 2
    else:
        new_proficiency = 1

    attempt.status = AssessmentAttempt.Status.EVALUATED
    attempt.score = total_earned_marks
    attempt.percentage = round(percentage, 2)
    attempt.submitted_at = timezone.now()
    attempt.save()

    # Create AssessmentResult record
    result, _ = AssessmentResult.objects.update_or_create(
        attempt=attempt,
        defaults={
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'incorrect_answers': incorrect_count,
            'unanswered': unanswered_count,
            'total_marks': total_possible_marks,
            'marks_obtained': total_earned_marks,
            'percentage': round(percentage, 2),
            'skill_level': new_proficiency
        }
    )

    # Update Student Skill & log history
    student_profile = attempt.student

    for ans in answers:
        skill_obj = ans.question.skill
        student_skill, created = StudentSkill.objects.get_or_create(
            student=student_profile,
            skill=skill_obj,
            defaults={'proficiency': new_proficiency, 'confidence': 0.85, 'source': StudentSkill.SourceChoice.ASSESSMENT_RESULT}
        )
        if not created:
            old_prof = student_skill.proficiency
            updated_prof = max(old_prof, new_proficiency)
            student_skill.proficiency = updated_prof
            student_skill.confidence = min(1.0, student_skill.confidence + 0.15)
            student_skill.source = StudentSkill.SourceChoice.ASSESSMENT_RESULT
            student_skill.save()

            StudentSkillHistory.objects.create(
                student=student_profile,
                skill=skill_obj,
                old_proficiency=old_prof,
                new_proficiency=updated_prof,
                change_source=StudentSkill.SourceChoice.ASSESSMENT_RESULT,
                reference_id=attempt.id
            )

    return attempt

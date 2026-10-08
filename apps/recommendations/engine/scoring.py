from django.conf import settings

def get_weights():
    return getattr(settings, 'RECOMMENDATION_WEIGHTS', {
        'CAREER_MATCH': 0.30,
        'SKILL_GAP': 0.25,
        'INTEREST_MATCH': 0.15,
        'BRANCH_MATCH': 0.10,
        'SEMESTER_MATCH': 0.10,
        'DIFFICULTY_MATCH': 0.05,
        'CONTENT_SIMILARITY': 0.05,
    })


def calculate_course_score(student_profile, course, content_sim_score, prereq_info):
    weights = get_weights()

    # 1. Skill Gap Score (0.0 to 1.0)
    student_skills_map = {ss.skill_id: ss.proficiency for ss in student_profile.skills.all()}
    primary_career = student_profile.career_goals.filter(is_primary=True).first()
    
    taught_skills = {cs.skill_id for cs in course.skills.all()}
    gap_skills = set()

    if primary_career:
        for req in primary_career.career.required_skills.all():
            curr_level = student_skills_map.get(req.skill_id, 0)
            if curr_level < req.required_level:
                gap_skills.add(req.skill_id)

    if gap_skills and taught_skills.intersection(gap_skills):
        skill_gap_score = min(1.0, len(taught_skills.intersection(gap_skills)) / len(gap_skills))
    elif taught_skills:
        skill_gap_score = 0.5
    else:
        skill_gap_score = 0.3

    # 2. Career Match Score (0.0 to 1.0)
    if primary_career:
        req_skills = {req.skill_id for req in primary_career.career.required_skills.all()}
        if req_skills and taught_skills.intersection(req_skills):
            career_score = min(1.0, 0.5 + (len(taught_skills.intersection(req_skills)) / len(req_skills)) * 0.5)
        else:
            career_score = 0.3
    else:
        career_score = 0.5

    # 3. Interest Match Score (0.0 to 1.0)
    student_interests = {si.interest_id for si in student_profile.interests.all()}
    interest_score = 0.8 if student_interests else 0.5

    # 4. Branch Match Score (0.0 to 1.0)
    branch_score = 1.0 if student_profile.branch_id else 0.7

    # 5. Semester Match Score (0.0 to 1.0)
    sem = student_profile.current_semester if student_profile.current_semester else 4
    diff = course.difficulty
    if sem <= 2 and diff == 'Beginner':
        semester_score = 1.0
    elif 3 <= sem <= 6 and diff in ('Beginner', 'Intermediate'):
        semester_score = 1.0
    elif sem >= 7 and diff in ('Intermediate', 'Advanced'):
        semester_score = 1.0
    else:
        semester_score = 0.7

    # 6. Difficulty Match Score (0.0 to 1.0)
    difficulty_score = 1.0

    # 7. Content Similarity (0.0 to 1.0)
    content_similarity = max(0.0, min(1.0, content_sim_score)) if content_sim_score > 0 else 0.6

    # Composite 7-factor weighted score (0-100 scale)
    raw_score = (
        weights.get('CAREER_MATCH', 0.30) * career_score +
        weights.get('SKILL_GAP', 0.25) * skill_gap_score +
        weights.get('INTEREST_MATCH', 0.15) * interest_score +
        weights.get('BRANCH_MATCH', 0.10) * branch_score +
        weights.get('SEMESTER_MATCH', 0.10) * semester_score +
        weights.get('DIFFICULTY_MATCH', 0.05) * difficulty_score +
        weights.get('CONTENT_SIMILARITY', 0.05) * content_similarity
    ) * 100.0

    penalty = prereq_info.get('penalty', 0.0)
    final_score = max(0.0, min(100.0, round(raw_score - penalty, 1)))

    return {
        "final_score": final_score,
        "skill_score": round(skill_gap_score * 100, 1),
        "career_score": round(career_score * 100, 1),
        "interest_score": round(interest_score * 100, 1),
        "branch_score": round(branch_score * 100, 1),
        "semester_score": round(semester_score * 100, 1),
        "difficulty_score": round(difficulty_score * 100, 1),
        "preference_score": round(content_similarity * 100, 1),
        "prerequisite_penalty": round(penalty, 1)
    }

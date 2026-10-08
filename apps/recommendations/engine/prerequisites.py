from apps.learning.models import StudentCourse

def evaluate_prerequisites(student_profile, course):
    prereqs = course.prerequisites.all().select_related('required_skill')
    if not prereqs:
        return {"satisfied": True, "missing_prerequisites": [], "penalty": 0.0}

    # Student skills lookup
    student_skills_map = {
        ss.skill_id: ss.proficiency for ss in student_profile.skills.all()
    }

    missing_items = []
    total_prereqs = 0
    missing_prereqs_count = 0

    for prereq in prereqs:
        total_prereqs += 1
        if prereq.required_skill_id:
            min_lvl = prereq.minimum_level or 1
            curr_lvl = student_skills_map.get(prereq.required_skill_id, 0)
            if curr_lvl < min_lvl:
                missing_prereqs_count += 1
                missing_items.append(f"Skill: {prereq.required_skill.name} (Need Level {min_lvl}, Current {curr_lvl})")

    # Penalty calculation
    if total_prereqs == 0 or missing_prereqs_count == 0:
        penalty = 0.0
    else:
        ratio = missing_prereqs_count / total_prereqs
        if ratio <= 0.25:
            penalty = 5.0
        elif ratio <= 0.50:
            penalty = 12.0
        elif ratio <= 0.75:
            penalty = 20.0
        else:
            penalty = 30.0

    return {
        "satisfied": missing_prereqs_count == 0,
        "missing_prerequisites": missing_items,
        "penalty": penalty
    }

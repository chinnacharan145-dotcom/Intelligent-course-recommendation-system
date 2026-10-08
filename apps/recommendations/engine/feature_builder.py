def build_student_feature_text(student_profile):
    tokens = []

    # Branch
    if student_profile.branch:
        tokens.append(student_profile.branch.name)
        tokens.append(student_profile.branch.code)

    # Semester
    if getattr(student_profile, 'current_semester', None):
        tokens.append(f"semester_{student_profile.current_semester}")

    # Skills (weighted by proficiency)
    for ss in student_profile.skills.all():
        skill_name = ss.skill.name.lower()
        tokens.extend([skill_name] * ss.proficiency)

    # Interests (weighted by priority)
    priority_weights = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'VERY_HIGH': 4}
    for si in student_profile.interests.all():
        interest_name = si.interest.name.lower()
        weight = priority_weights.get(si.priority, 2)
        tokens.extend([interest_name] * weight)

    # Career Goals
    for cg in student_profile.career_goals.all():
        career_name = cg.career.name.lower()
        weight = 5 if cg.is_primary else 2
        tokens.extend([career_name] * weight)
        for req in cg.career.required_skills.all():
            tokens.append(req.skill.name.lower())

    pref_diff = getattr(student_profile, 'preferred_difficulty', None)
    if pref_diff:
        tokens.append(pref_diff.lower())

    return " ".join(tokens)


def build_course_feature_text(course):
    tokens = [
        course.title.lower(),
        course.description.lower() if course.description else "",
        course.category.name.lower() if course.category else "",
        course.provider.name.lower() if course.provider else "",
        course.difficulty.lower() if course.difficulty else ""
    ]

    # Skills taught
    for cs in course.skills.all():
        tokens.append(cs.skill.name.lower())

    return " ".join(tokens)

def generate_recommendation_explanation(student_profile, course, scores, prereq_info):
    reasons = []

    primary_career = student_profile.career_goals.filter(is_primary=True).first()
    if primary_career and scores.get('career_score', 0) >= 70.0:
        reasons.append(f"✓ Matches your target career: {primary_career.career.name}")

    if scores.get('skill_score', 0) >= 60.0:
        skills_taught = [cs.skill.name for cs in course.skills.all()]
        if skills_taught:
            reasons.append(f"✓ Addresses key skill gap: {', '.join(skills_taught[:3])}")

    if scores.get('interest_score', 0) >= 70.0:
        reasons.append("✓ Aligns with your specified interest categories")

    if student_profile.branch and scores.get('branch_score', 0) >= 70.0:
        reasons.append(f"✓ Relevant for {student_profile.branch.code} curriculum")

    if not reasons:
        reasons.append("✓ Highly rated course matching your overall academic profile")

    warnings = []
    if not prereq_info.get('satisfied', True):
        for missing_item in prereq_info.get('missing_prerequisites', []):
            warnings.append(f"⚠ Recommended before starting: {missing_item}")

    explanation_data = {
        "summary": f"Recommended with {scores['final_score']}% match score.",
        "reasons": reasons,
        "warnings": warnings,
        "scores_breakdown": {
            "career_match": scores.get('career_score', 0),
            "skill_gap": scores.get('skill_score', 0),
            "interest_match": scores.get('interest_score', 0),
            "branch_match": scores.get('branch_score', 0),
            "semester_match": scores.get('semester_score', 0),
            "difficulty_match": scores.get('difficulty_score', 0),
            "content_similarity": scores.get('similarity_score', 0),
            "prerequisite_penalty": scores.get('prerequisite_penalty', 0)
        }
    }

    return explanation_data

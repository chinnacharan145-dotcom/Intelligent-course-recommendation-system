from .models import Skill, SkillPrerequisite

def get_skill_prerequisite_dag(skill_id, visited=None):
    """
    Recursively builds the prerequisite dependency graph for a given skill.
    """
    if visited is None:
        visited = set()

    if skill_id in visited:
        return []
    visited.add(skill_id)

    prereqs = SkillPrerequisite.objects.filter(skill_id=skill_id).select_related('prerequisite_skill', 'prerequisite_skill__category')
    graph = []

    for item in prereqs:
        p_skill = item.prerequisite_skill
        graph.append({
            "skill_id": str(p_skill.id),
            "skill_name": p_skill.name,
            "category": p_skill.category.name if p_skill.category else None,
            "minimum_level": item.minimum_level,
            "is_mandatory": item.is_mandatory,
            "sub_prerequisites": get_skill_prerequisite_dag(p_skill.id, visited.copy())
        })

    return graph


def get_skill_dependents(skill_id):
    """
    Returns skills that directly depend on the given skill.
    """
    dependents = SkillPrerequisite.objects.filter(prerequisite_skill_id=skill_id).select_related('skill', 'skill__category')
    return [
        {
            "skill_id": str(dep.skill.id),
            "skill_name": dep.skill.name,
            "category": dep.skill.category.name if dep.skill.category else None,
            "minimum_level": dep.minimum_level
        }
        for dep in dependents
    ]

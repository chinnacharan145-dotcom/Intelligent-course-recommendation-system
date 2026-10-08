from apps.recommendations.models import Recommendation, RecommendationReason
from .candidate_filter import get_candidate_courses
from .feature_builder import build_student_feature_text, build_course_feature_text
from .similarity import calculate_content_similarities
from .prerequisites import evaluate_prerequisites
from .scoring import calculate_course_score
from .ranking import rank_recommendations
from .explanations import generate_recommendation_explanation

class HybridRecommender:
    ALGORITHM_VERSION = 'hybrid-v1'

    @classmethod
    def generate_recommendations(cls, student_profile, top_n=10, refresh=False):
        if not refresh:
            cached_recs = Recommendation.objects.filter(
                student=student_profile,
                status=Recommendation.Status.ACTIVE
            ).select_related('course', 'course__provider', 'course__category').prefetch_related('reasons').order_by('-match_score')[:top_n]
            
            if cached_recs.exists():
                return list(cached_recs)

        # 1. Candidate Filtering
        candidates = get_candidate_courses(student_profile)
        if not candidates:
            return []

        # 2. Feature Building & Vectorization
        student_text = build_student_feature_text(student_profile)
        course_texts = [build_course_feature_text(c) for c in candidates]
        
        # 3. Content Similarity
        similarities = calculate_content_similarities(student_text, course_texts)

        # 4. Multi-factor Scoring & Prerequisite Evaluation
        scored_items = []
        primary_goal = student_profile.career_goals.filter(is_primary=True).first()
        target_career = primary_goal.career if primary_goal else None

        for idx, course in enumerate(candidates):
            sim_score = similarities[idx]
            prereq_info = evaluate_prerequisites(student_profile, course)
            scores = calculate_course_score(student_profile, course, sim_score, prereq_info)
            explanation = generate_recommendation_explanation(student_profile, course, scores, prereq_info)
            
            scored_items.append({
                "course": course,
                "scores": scores,
                "prereq_info": prereq_info,
                "explanation": explanation
            })

        # 5. Ranking
        ranked_items = rank_recommendations(scored_items, top_n=top_n)

        # 6. Database Storage
        Recommendation.objects.filter(student=student_profile, status=Recommendation.Status.ACTIVE).delete()

        created_recs = []
        for item in ranked_items:
            course = item['course']
            scores = item['scores']
            explanation = item['explanation']

            rec = Recommendation.objects.create(
                student=student_profile,
                course=course,
                career=target_career,
                match_score=scores['final_score'],
                career_match_score=scores['career_score'],
                skill_match_score=scores['skill_score'],
                branch_match_score=scores['branch_score'],
                difficulty_match_score=scores['difficulty_score'],
                content_similarity_score=scores['preference_score'],
                status=Recommendation.Status.ACTIVE
            )

            # Persist explanation reasons
            for idx, reason_str in enumerate(explanation.get('reasons', [])):
                RecommendationReason.objects.create(
                    recommendation=rec,
                    reason_type='SCORE_FACTOR',
                    reason_text=reason_str,
                    priority=idx + 1
                )

            for idx, warning_str in enumerate(explanation.get('warnings', [])):
                RecommendationReason.objects.create(
                    recommendation=rec,
                    reason_type='PREREQUISITE_WARNING',
                    reason_text=warning_str,
                    priority=100 + idx
                )

            created_recs.append(rec)

        return list(Recommendation.objects.filter(student=student_profile, status=Recommendation.Status.ACTIVE).select_related('course', 'course__provider', 'course__category').prefetch_related('reasons').order_by('-match_score'))

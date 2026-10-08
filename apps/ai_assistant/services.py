import os
import json
import urllib.request
from django.conf import settings

class GeminiAssistantService:
    @classmethod
    def get_api_key(cls):
        return getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')

    @classmethod
    def explain_recommendation_with_ai(cls, recommendation):
        api_key = cls.get_api_key()
        
        reasons = [r.reason_text for r in recommendation.reasons.filter(reason_type='SCORE_FACTOR')]
        warnings = [r.reason_text for r in recommendation.reasons.filter(reason_type='PREREQUISITE_WARNING')]
        course_title = recommendation.course.title
        match_score = float(recommendation.match_score)

        deterministic_text = (
            f"Course '{course_title}' is recommended with a {match_score}% match score. "
            + " ".join(reasons)
            + (" " + " ".join(warnings) if warnings else "")
        )

        if not api_key:
            return {
                "source": "DETERMINISTIC_RULES",
                "explanation_text": deterministic_text,
                "reasons": reasons,
                "warnings": warnings
            }

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            prompt = (
                "You are an encouraging academic advisor for engineering students. "
                "Rewrite the following recommendation facts into 2 friendly, motivating bullet points. "
                "Do NOT invent facts outside the evidence.\n"
                f"Course: {course_title}\n"
                f"Match Score: {match_score}%\n"
                f"Reasons: {json.dumps(reasons)}\n"
                f"Warnings: {json.dumps(warnings)}\n"
            )
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                ai_text = res_data['candidates'][0]['content']['parts'][0]['text']

            return {
                "source": "GEMINI_AI",
                "explanation_text": ai_text.strip(),
                "reasons": reasons,
                "warnings": warnings
            }
        except Exception:
            return {
                "source": "DETERMINISTIC_FALLBACK",
                "explanation_text": deterministic_text,
                "reasons": reasons,
                "warnings": warnings
            }

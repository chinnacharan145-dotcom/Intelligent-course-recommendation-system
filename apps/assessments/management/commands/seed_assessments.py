from django.core.management.base import BaseCommand
from apps.assessments.models import Assessment, AssessmentQuestion, AssessmentOption
from apps.skills.models import Skill

class Command(BaseCommand):
    help = "Seed skill assessment tests, questions, options, and answers."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Skill Assessment Verification Engine...")

        assessments_data = [
            {
                "title": "Python Programming Proficiency Test",
                "description": "Evaluate Python core syntax, data types, functions, list comprehensions, and OOP.",
                "type": Assessment.Type.SKILL_LEVEL,
                "duration": 20,
                "passing_marks": 7.0,
                "skill_name": "Python",
                "questions": [
                    {
                        "text": "What is the output of len(set([1, 2, 2, 3, 4, 4, 4])) in Python?",
                        "difficulty": AssessmentQuestion.Difficulty.BEGINNER,
                        "marks": 2.0,
                        "options": [
                            ("3", False),
                            ("4", True),
                            ("7", False),
                            ("TypeError", False)
                        ]
                    },
                    {
                        "text": "Which of the following is a mutable data type in Python?",
                        "difficulty": AssessmentQuestion.Difficulty.BEGINNER,
                        "marks": 2.0,
                        "options": [
                            ("Tuple", False),
                            ("String", False),
                            ("List", True),
                            ("Integer", False)
                        ]
                    },
                    {
                        "text": "What decorator is used in Python OOP to define a class method?",
                        "difficulty": AssessmentQuestion.Difficulty.INTERMEDIATE,
                        "marks": 3.0,
                        "options": [
                            ("@staticmethod", False),
                            ("@classmethod", True),
                            ("@property", False),
                            ("@abstractmethod", False)
                        ]
                    },
                    {
                        "text": "What does a generator function return when called in Python?",
                        "difficulty": AssessmentQuestion.Difficulty.INTERMEDIATE,
                        "marks": 3.0,
                        "options": [
                            ("A list of values", False),
                            ("A generator object containing an iterator", True),
                            ("A tuple of values", False),
                            ("None", False)
                        ]
                    }
                ]
            },
            {
                "title": "Data Structures & Algorithms Diagnostic Test",
                "description": "Test fundamental algorithm complexity, binary trees, sorting, and dynamic programming.",
                "type": Assessment.Type.DIAGNOSTIC,
                "duration": 30,
                "passing_marks": 7.0,
                "skill_name": "Data Structures",
                "questions": [
                    {
                        "text": "What is the worst-case time complexity of QuickSort?",
                        "difficulty": AssessmentQuestion.Difficulty.INTERMEDIATE,
                        "marks": 2.5,
                        "options": [
                            ("O(N log N)", False),
                            ("O(N^2)", True),
                            ("O(N)", False),
                            ("O(1)", False)
                        ]
                    },
                    {
                        "text": "Which data structure follows First-In, First-Out (FIFO) principle?",
                        "difficulty": AssessmentQuestion.Difficulty.BEGINNER,
                        "marks": 2.5,
                        "options": [
                            ("Stack", False),
                            ("Queue", True),
                            ("Tree", False),
                            ("Graph", False)
                        ]
                    },
                    {
                        "text": "What is the height of a balanced Binary Search Tree with N nodes?",
                        "difficulty": AssessmentQuestion.Difficulty.INTERMEDIATE,
                        "marks": 2.5,
                        "options": [
                            ("O(log N)", True),
                            ("O(N)", False),
                            ("O(N log N)", False),
                            ("O(1)", False)
                        ]
                    },
                    {
                        "text": "Which algorithm finds the shortest path in a weighted graph without negative edges?",
                        "difficulty": AssessmentQuestion.Difficulty.ADVANCED,
                        "marks": 2.5,
                        "options": [
                            ("Dijkstra's Algorithm", True),
                            ("Depth First Search", False),
                            ("Kruskal's Algorithm", False),
                            ("Floyd-Warshall", False)
                        ]
                    }
                ]
            }
        ]

        for adata in assessments_data:
            total_m = sum(q["marks"] for q in adata["questions"])
            assessment, _ = Assessment.objects.get_or_create(
                title=adata["title"],
                defaults={
                    "description": adata["description"],
                    "assessment_type": adata["type"],
                    "duration_minutes": adata["duration"],
                    "total_marks": total_m,
                    "passing_marks": adata["passing_marks"]
                }
            )

            skill_obj = Skill.objects.filter(name=adata["skill_name"]).first()

            for idx, qdata in enumerate(adata["questions"], start=1):
                if skill_obj:
                    q_obj, _ = AssessmentQuestion.objects.get_or_create(
                        assessment=assessment,
                        question_text=qdata["text"],
                        defaults={
                            "skill": skill_obj,
                            "marks": qdata["marks"],
                            "difficulty": qdata["difficulty"],
                            "question_order": idx
                        }
                    )

                    for o_idx, (o_text, is_corr) in enumerate(qdata["options"], start=1):
                        AssessmentOption.objects.get_or_create(
                            question=q_obj,
                            option_text=o_text,
                            defaults={
                                "is_correct": is_corr,
                                "option_order": o_idx
                            }
                        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Assessments & Questions!"))

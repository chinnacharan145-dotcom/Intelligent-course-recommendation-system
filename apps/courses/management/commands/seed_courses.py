from django.core.management.base import BaseCommand
from apps.courses.models import CourseProvider, CourseCategory, Course, CourseSkill, CoursePrerequisite
from apps.skills.models import Skill

class Command(BaseCommand):
    help = "Seed course providers, categories, engineering courses, taught skills, and course prerequisites."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Courses & Content Intelligence...")

        # 1. Providers
        providers_data = [
            ("Coursera", "https://coursera.org", "Global online learning platform featuring university courses."),
            ("NPTEL", "https://nptel.ac.in", "National Programme on Technology Enhanced Learning by IITs & IISc."),
            ("edX", "https://edx.org", "Online learning platform founded by Harvard and MIT."),
            ("MIT OpenCourseWare", "https://ocw.mit.edu", "Free publication of MIT course materials."),
            ("Udemy", "https://udemy.com", "Online learning and teaching marketplace."),
            ("Fast.ai", "https://fast.ai", "Making neural nets uncool again with practical deep learning courses.")
        ]
        prov_objs = {}
        for name, url, desc in providers_data:
            p, _ = CourseProvider.objects.get_or_create(name=name, defaults={"website": url, "description": desc})
            prov_objs[name] = p

        # 2. Categories
        cat_data = [
            ("Computer Science & Software", "Core computer science and programming fundamentals."),
            ("AI, ML & Data Science", "Machine learning, artificial intelligence, and statistics."),
            ("Web & Mobile Engineering", "Full stack development, APIs, frontend and backend."),
            ("Cloud, DevOps & Systems", "System administration, cloud architecture, and containers."),
            ("Core Engineering & Math", "Electrical, mechanical, civil, and applied mathematics.")
        ]
        cat_objs = {}
        for name, desc in cat_data:
            c, _ = CourseCategory.objects.get_or_create(name=name, defaults={"description": desc})
            cat_objs[name] = c

        # 3. Courses
        courses = [
            {
                "title": "Machine Learning Specialization by Andrew Ng",
                "provider": prov_objs["Coursera"],
                "category": cat_objs["AI, ML & Data Science"],
                "difficulty": Course.Difficulty.INTERMEDIATE,
                "duration_hours": 40.0,
                "rating": 4.90,
                "is_free": True,
                "url": "https://coursera.org/specializations/machine-learning-introduction",
                "description": "Master fundamental machine learning concepts using Python, NumPy, and scikit-learn.",
                "taught_skills": [("Machine Learning", 4), ("Python", 4), ("Linear Algebra", 3)],
                "prereqs": [("Python", 2), ("Linear Algebra", 2)]
            },
            {
                "title": "Deep Learning Specialization",
                "provider": prov_objs["Coursera"],
                "category": cat_objs["AI, ML & Data Science"],
                "difficulty": Course.Difficulty.ADVANCED,
                "duration_hours": 60.0,
                "rating": 4.95,
                "is_free": False,
                "url": "https://coursera.org/specializations/deep-learning",
                "description": "Build and train neural networks, CNNs, RNNs, and Transformers with PyTorch and TensorFlow.",
                "taught_skills": [("Deep Learning", 4), ("Natural Language Processing", 3), ("Computer Vision", 3)],
                "prereqs": [("Machine Learning", 3), ("Python", 3)]
            },
            {
                "title": "Practical Deep Learning for Coders",
                "provider": prov_objs["Fast.ai"],
                "category": cat_objs["AI, ML & Data Science"],
                "difficulty": Course.Difficulty.INTERMEDIATE,
                "duration_hours": 35.0,
                "rating": 4.85,
                "is_free": True,
                "url": "https://course.fast.ai",
                "description": "A top-down, hands-on deep learning course for computer programmers.",
                "taught_skills": [("Deep Learning", 4), ("Python", 4), ("Computer Vision", 3)],
                "prereqs": [("Python", 3)]
            },
            {
                "title": "NPTEL: Data Structures and Algorithms in Python",
                "provider": prov_objs["NPTEL"],
                "category": cat_objs["Computer Science & Software"],
                "difficulty": Course.Difficulty.BEGINNER,
                "duration_hours": 30.0,
                "rating": 4.70,
                "is_free": True,
                "url": "https://nptel.ac.in/courses/106106145",
                "description": "Comprehensive data structures and algorithm analysis taught by IIT professors.",
                "taught_skills": [("Data Structures", 4), ("Algorithms", 4), ("Python", 3)],
                "prereqs": [("Python", 2)]
            },
            {
                "title": "NPTEL: Database Management System",
                "provider": prov_objs["NPTEL"],
                "category": cat_objs["Computer Science & Software"],
                "difficulty": Course.Difficulty.INTERMEDIATE,
                "duration_hours": 30.0,
                "rating": 4.65,
                "is_free": True,
                "url": "https://nptel.ac.in/courses/106105175",
                "description": "Relational database design, ER modeling, SQL querying, indexing, and transactions.",
                "taught_skills": [("SQL", 4), ("Database Systems", 4)],
                "prereqs": []
            },
            {
                "title": "Full Stack Web Development with React & Node",
                "provider": prov_objs["Udemy"],
                "category": cat_objs["Web & Mobile Engineering"],
                "difficulty": Course.Difficulty.BEGINNER,
                "duration_hours": 45.0,
                "rating": 4.80,
                "is_free": False,
                "url": "https://udemy.com/full-stack-react-node",
                "description": "Build complete full-stack web applications with React frontend and Node.js backend.",
                "taught_skills": [("React.js", 4), ("Node.js", 4), ("JavaScript", 4), ("HTML & CSS", 3)],
                "prereqs": [("JavaScript", 2)]
            },
            {
                "title": "Docker & Kubernetes: The Complete Guide",
                "provider": prov_objs["Udemy"],
                "category": cat_objs["Cloud, DevOps & Systems"],
                "difficulty": Course.Difficulty.INTERMEDIATE,
                "duration_hours": 22.0,
                "rating": 4.75,
                "is_free": False,
                "url": "https://udemy.com/docker-and-kubernetes-the-complete-guide",
                "description": "Containerize web apps with Docker and manage microservices with Kubernetes.",
                "taught_skills": [("Docker", 4), ("Kubernetes", 4), ("Linux System Admin", 3)],
                "prereqs": [("Linux System Admin", 2)]
            }
        ]

        for cdata in courses:
            course_obj, _ = Course.objects.get_or_create(
                title=cdata["title"],
                defaults={
                    "provider": cdata["provider"],
                    "category": cdata["category"],
                    "difficulty": cdata["difficulty"],
                    "duration_hours": cdata["duration_hours"],
                    "rating": cdata["rating"],
                    "is_free": cdata["is_free"],
                    "url": cdata["url"],
                    "description": cdata["description"]
                }
            )

            # Taught Skills
            for skill_name, lvl in cdata["taught_skills"]:
                s = Skill.objects.filter(name=skill_name).first()
                if s:
                    CourseSkill.objects.get_or_create(
                        course=course_obj,
                        skill=s,
                        defaults={"level": lvl}
                    )

            # Prerequisite Skills
            for skill_name, min_lvl in cdata["prereqs"]:
                s = Skill.objects.filter(name=skill_name).first()
                if s:
                    CoursePrerequisite.objects.get_or_create(
                        course=course_obj,
                        required_skill=s,
                        defaults={"minimum_level": min_lvl, "is_mandatory": True}
                    )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Courses & Content Intelligence!"))

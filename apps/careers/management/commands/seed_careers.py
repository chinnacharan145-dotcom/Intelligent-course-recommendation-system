from django.core.management.base import BaseCommand
from apps.careers.models import Career, CareerSkill
from apps.skills.models import Skill

class Command(BaseCommand):
    help = "Seed engineering career roles and skill requirement mappings."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Career Roles & Skill Requirements...")

        careers_data = [
            {
                "name": "Artificial Intelligence & Machine Learning Engineer",
                "slug": "ai-ml-engineer",
                "industry": "Artificial Intelligence",
                "salary_min": 800000.00,
                "salary_max": 2400000.00,
                "description": "Designs, builds, and deploys scalable machine learning models and neural network systems.",
                "skills": [
                    ("Python", 4, 5, True),
                    ("Machine Learning", 4, 5, True),
                    ("Deep Learning", 3, 4, True),
                    ("Linear Algebra", 3, 3, False),
                    ("Probability & Statistics", 3, 4, True),
                    ("SQL", 3, 3, False)
                ]
            },
            {
                "name": "Full Stack Web Developer",
                "slug": "full-stack-developer",
                "industry": "Software Engineering",
                "salary_min": 600000.00,
                "salary_max": 1800000.00,
                "description": "Develops responsive frontend user interfaces and robust backend REST APIs.",
                "skills": [
                    ("JavaScript", 4, 5, True),
                    ("HTML & CSS", 3, 4, True),
                    ("React.js", 3, 4, True),
                    ("Node.js", 3, 4, True),
                    ("Django Framework", 3, 4, False),
                    ("SQL", 3, 3, True),
                    ("Git & GitHub", 3, 3, True)
                ]
            },
            {
                "name": "Data Engineer",
                "slug": "data-engineer",
                "industry": "Data Engineering",
                "salary_min": 750000.00,
                "salary_max": 2200000.00,
                "description": "Builds and maintains large-scale data pipelines, ETL workflows, and data platforms.",
                "skills": [
                    ("Python", 4, 5, True),
                    ("SQL", 4, 5, True),
                    ("Data Engineering", 3, 5, True),
                    ("Database Systems", 3, 4, True),
                    ("Docker", 3, 3, False)
                ]
            },
            {
                "name": "Cloud & DevOps Engineer",
                "slug": "devops-engineer",
                "industry": "Cloud Computing",
                "salary_min": 700000.00,
                "salary_max": 2000000.00,
                "description": "Automates CI/CD pipelines, container orchestration, and multi-cloud infrastructure.",
                "skills": [
                    ("Docker", 4, 5, True),
                    ("Kubernetes", 3, 5, True),
                    ("Linux System Admin", 4, 4, True),
                    ("AWS Cloud", 3, 4, True),
                    ("Git & GitHub", 4, 4, True)
                ]
            },
            {
                "name": "Embedded Systems Engineer",
                "slug": "embedded-engineer",
                "industry": "Hardware & Systems",
                "salary_min": 600000.00,
                "salary_max": 1600000.00,
                "description": "Programs microcontrollers, real-time operating systems, and IoT hardware.",
                "skills": [
                    ("C++", 4, 5, True),
                    ("Operating Systems", 3, 4, True),
                    ("Computer Networks", 3, 3, False)
                ]
            }
        ]

        for cdata in careers_data:
            career, _ = Career.objects.get_or_create(
                slug=cdata["slug"],
                defaults={
                    "name": cdata["name"],
                    "industry": cdata["industry"],
                    "salary_min": cdata["salary_min"],
                    "salary_max": cdata["salary_max"],
                    "description": cdata["description"]
                }
            )

            for skill_name, req_lvl, imp, is_req in cdata["skills"]:
                skill_obj = Skill.objects.filter(name=skill_name).first()
                if skill_obj:
                    CareerSkill.objects.get_or_create(
                        career=career,
                        skill=skill_obj,
                        defaults={
                            "required_level": req_lvl,
                            "importance": imp,
                            "required": is_req
                        }
                    )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Careers & Skill Requirements!"))

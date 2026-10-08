from django.core.management.base import BaseCommand
from apps.skills.models import SkillCategory, Skill, SkillPrerequisite, Interest

class Command(BaseCommand):
    help = "Seed initial skill categories, technical skills, skill prerequisites, and student interests."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Skill Taxonomy & Graph...")

        # 1. Skill Categories
        cat_data = [
            ("Programming Languages", "Core software development languages"),
            ("Data Science & AI", "Machine learning, deep learning, statistics, data engineering"),
            ("Web & Mobile Development", "Frontend, backend, mobile app frameworks"),
            ("Cloud & DevOps", "Cloud platforms, containers, CI/CD, infrastructure"),
            ("Core Engineering", "Data structures, algorithms, operating systems, networking"),
            ("Soft Skills & Management", "Leadership, communication, project management")
        ]
        cat_objs = {}
        for name, desc in cat_data:
            c, _ = SkillCategory.objects.get_or_create(name=name, defaults={"description": desc})
            cat_objs[name] = c

        # 2. Skills
        skills_data = [
            # Programming
            ("Python", "Python", cat_objs["Programming Languages"], "High-level dynamic programming language for AI & web."),
            ("Java", "Java", cat_objs["Programming Languages"], "Object-oriented language widely used in enterprise apps."),
            ("C++", "CPP", cat_objs["Programming Languages"], "Performance-critical system programming language."),
            ("JavaScript", "JS", cat_objs["Programming Languages"], "Core scripting language of the web."),
            ("TypeScript", "TS", cat_objs["Programming Languages"], "Typed superset of JavaScript."),
            ("SQL", "SQL", cat_objs["Programming Languages"], "Standard language for relational database querying."),

            # Core Engineering
            ("Data Structures", "DSA_DS", cat_objs["Core Engineering"], "Arrays, LinkedLists, Trees, Graphs, HashTables."),
            ("Algorithms", "DSA_ALG", cat_objs["Core Engineering"], "Sorting, Searching, Dynamic Programming, Greedy algorithms."),
            ("Operating Systems", "OS", cat_objs["Core Engineering"], "Process scheduling, concurrency, virtual memory."),
            ("Computer Networks", "CN", cat_objs["Core Engineering"], "TCP/IP, HTTP, DNS, Socket programming."),
            ("Database Systems", "DBMS", cat_objs["Core Engineering"], "ACID transactions, ER modeling, indexing."),

            # AI & Data Science
            ("Linear Algebra", "MATH_LA", cat_objs["Data Science & AI"], "Vectors, matrices, linear transformations."),
            ("Probability & Statistics", "MATH_STAT", cat_objs["Data Science & AI"], "Probability distributions, estimation, hypothesis testing."),
            ("Machine Learning", "ML", cat_objs["Data Science & AI"], "Supervised, unsupervised, feature engineering, scikit-learn."),
            ("Deep Learning", "DL", cat_objs["Data Science & AI"], "Neural networks, CNNs, RNNs, PyTorch, TensorFlow."),
            ("Natural Language Processing", "NLP", cat_objs["Data Science & AI"], "Tokenization, LLMs, Transformers, HuggingFace."),
            ("Computer Vision", "CV", cat_objs["Data Science & AI"], "Image processing, OpenCV, object detection, Segmentation."),
            ("Data Engineering", "DE", cat_objs["Data Science & AI"], "ETL pipelines, Spark, Kafka, Data Warehousing."),

            # Web & Mobile
            ("HTML & CSS", "WEB_BASE", cat_objs["Web & Mobile Development"], "Semantic web markup and modern CSS styling."),
            ("React.js", "REACT", cat_objs["Web & Mobile Development"], "Component-based UI library for web development."),
            ("Node.js", "NODE", cat_objs["Web & Mobile Development"], "Event-driven server-side JavaScript runtime."),
            ("Django Framework", "DJANGO", cat_objs["Web & Mobile Development"], "High-level Python web framework."),
            ("REST API Design", "REST_API", cat_objs["Web & Mobile Development"], "Designing scalable HTTP RESTful web services."),

            # Cloud & DevOps
            ("Docker", "DOCKER", cat_objs["Cloud & DevOps"], "Containerization platform for application packaging."),
            ("Kubernetes", "K8S", cat_objs["Cloud & DevOps"], "Container orchestration system."),
            ("AWS Cloud", "AWS", cat_objs["Cloud & DevOps"], "Amazon Web Services cloud architecture."),
            ("Git & GitHub", "GIT", cat_objs["Cloud & DevOps"], "Distributed version control system."),
            ("Linux System Admin", "LINUX", cat_objs["Cloud & DevOps"], "Bash scripting, process control, system security.")
        ]

        skill_objs = {}
        for name, code, cat, desc in skills_data:
            s, _ = Skill.objects.get_or_create(
                name=name,
                defaults={"code": code, "category": cat, "description": desc}
            )
            skill_objs[name] = s

        # 3. Prerequisites Graph
        prereqs = [
            ("Algorithms", "Data Structures", 2, True),
            ("Machine Learning", "Python", 3, True),
            ("Machine Learning", "Linear Algebra", 2, True),
            ("Machine Learning", "Probability & Statistics", 2, True),
            ("Deep Learning", "Machine Learning", 3, True),
            ("Natural Language Processing", "Deep Learning", 3, True),
            ("Computer Vision", "Deep Learning", 3, True),
            ("React.js", "JavaScript", 3, True),
            ("React.js", "HTML & CSS", 2, True),
            ("Node.js", "JavaScript", 3, True),
            ("Django Framework", "Python", 3, True),
            ("Django Framework", "SQL", 2, True),
            ("REST API Design", "HTTP & Web", 2, False),
            ("Kubernetes", "Docker", 3, True),
            ("Docker", "Linux System Admin", 2, False),
            ("Data Engineering", "SQL", 3, True),
            ("Data Engineering", "Python", 3, True),
        ]

        for skill_name, prereq_name, min_lvl, is_mand in prereqs:
            if skill_name in skill_objs and prereq_name in skill_objs:
                SkillPrerequisite.objects.get_or_create(
                    skill=skill_objs[skill_name],
                    prerequisite_skill=skill_objs[prereq_name],
                    defaults={"minimum_level": min_lvl, "is_mandatory": is_mand}
                )

        # 4. Student Interests
        interests_data = [
            ("Artificial Intelligence & Data Science", "Building intelligent ML & AI models"),
            ("Full Stack Web Development", "Building end-to-end web applications"),
            ("Cloud Architecture & DevOps", "Deploying and scaling cloud infrastructure"),
            ("Cybersecurity & Ethical Hacking", "Securing software systems and networks"),
            ("Mobile App Development", "Creating iOS & Android applications"),
            ("Blockchain & Web3", "Decentralized applications and smart contracts"),
            ("Embedded Systems & IoT", "Hardware programming, robotics, and sensors"),
            ("Game Development", "Graphics programming and 3D game engines"),
            ("Competitive Programming", "Solving complex algorithmic problems"),
            ("Open Source Contribution", "Contributing to global developer ecosystems")
        ]

        for name, desc in interests_data:
            Interest.objects.get_or_create(
                name=name,
                defaults={"description": desc}
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Skill Taxonomy & Graph!"))

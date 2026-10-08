from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.academics.models import University, College, Program, Branch, Regulation, Curriculum, Subject
from apps.skills.models import Skill, Interest
from apps.careers.models import Career, CareerSkill
from apps.courses.models import (
    CourseProvider, CourseCategory, Course, CourseSkill,
    CourseInterest, CourseCareer, CourseBranch, CoursePrerequisite
)
from apps.assessments.models import Assessment, Question, Option

class Command(BaseCommand):
    help = 'Seeds database with realistic AP Universities, Colleges, Regulations, Curricula, Skills, Careers, Courses & Assessments.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding process..."))

        # 1. Universities
        jntua, _ = University.objects.get_or_create(
            short_name='JNTUA',
            defaults={
                'name': 'Jawaharlal Nehru Technological University Anantapur',
                'university_type': University.UniversityType.STATE,
                'state': 'Andhra Pradesh',
                'website': 'https://jntua.ac.in'
            }
        )
        jntuk, _ = University.objects.get_or_create(
            short_name='JNTUK',
            defaults={
                'name': 'Jawaharlal Nehru Technological University Kakinada',
                'university_type': University.UniversityType.STATE,
                'state': 'Andhra Pradesh',
                'website': 'https://jntuk.edu.in'
            }
        )
        au, _ = University.objects.get_or_create(
            short_name='AU',
            defaults={
                'name': 'Andhra University College of Engineering',
                'university_type': University.UniversityType.STATE,
                'state': 'Andhra Pradesh',
                'website': 'https://andhrauniversity.edu.in'
            }
        )
        vignan, _ = University.objects.get_or_create(
            short_name='VFSTR',
            defaults={
                'name': "Vignan's Foundation for Science, Technology and Research",
                'university_type': University.UniversityType.DEEMED,
                'state': 'Andhra Pradesh',
                'website': 'https://vignan.ac.in'
            }
        )

        self.stdout.write("-> Universities seeded.")

        # 2. Colleges
        colleges_data = [
            {'code': 'JNTUACEA', 'name': 'JNTUA College of Engineering Anantapur', 'university': jntua, 'district': 'Anantapur', 'city': 'Anantapur', 'autonomous': True},
            {'code': 'JNTUACEK', 'name': 'JNTUK College of Engineering Kakinada', 'university': jntuk, 'district': 'Kakinada', 'city': 'Kakinada', 'autonomous': True},
            {'code': 'AUCE', 'name': 'Andhra University College of Engineering Visakhapatnam', 'university': au, 'district': 'Visakhapatnam', 'city': 'Visakhapatnam', 'autonomous': True},
            {'code': 'VRSEC', 'name': 'Velagapudi Ramakrishna Siddhartha Engineering College', 'university': jntuk, 'district': 'NTR Vijayawada', 'city': 'Vijayawada', 'autonomous': True},
            {'code': 'GVPCE', 'name': 'Gayatri Vidya Parishad College of Engineering', 'university': jntuk, 'district': 'Visakhapatnam', 'city': 'Visakhapatnam', 'autonomous': True},
            {'code': 'RVRJC', 'name': 'RVR & JC College of Engineering', 'university': jntuk, 'district': 'Guntur', 'city': 'Guntur', 'autonomous': True},
            {'code': 'SRKR', 'name': 'Sagi Ramakrishnam Raju Engineering College', 'university': jntuk, 'district': 'West Godavari', 'city': 'Bhimavaram', 'autonomous': True},
            {'code': 'VVIT', 'name': 'Vasireddy Venkatadri Institute of Technology', 'university': jntuk, 'district': 'Guntur', 'city': 'Nambur', 'autonomous': True},
        ]
        colleges_dict = {}
        for cdata in colleges_data:
            c_obj, _ = College.objects.get_or_create(code=cdata['code'], defaults=cdata)
            colleges_dict[cdata['code']] = c_obj

        self.stdout.write("-> Colleges seeded.")

        # 3. Programs & Branches
        btech, _ = Program.objects.get_or_create(short_name='B.Tech', defaults={'name': 'Bachelor of Technology', 'duration_years': 4})
        
        branches_data = [
            {'code': 'CSE', 'name': 'Computer Science and Engineering'},
            {'code': 'CSE-AIML', 'name': 'CSE (Artificial Intelligence & Machine Learning)'},
            {'code': 'CSE-DS', 'name': 'CSE (Data Science)'},
            {'code': 'AIDS', 'name': 'Artificial Intelligence and Data Science'},
            {'code': 'IT', 'name': 'Information Technology'},
            {'code': 'ECE', 'name': 'Electronics and Communication Engineering'},
            {'code': 'EEE', 'name': 'Electrical and Electronics Engineering'},
            {'code': 'MECH', 'name': 'Mechanical Engineering'},
            {'code': 'CIVIL', 'name': 'Civil Engineering'},
        ]
        branches_dict = {}
        for bdata in branches_data:
            b_obj, _ = Branch.objects.get_or_create(code=bdata['code'], defaults=bdata)
            branches_dict[bdata['code']] = b_obj

        self.stdout.write("-> Branches seeded.")

        # 4. Regulations
        r20_jntua, _ = Regulation.objects.get_or_create(name='R20', university=jntua, defaults={'effective_from_year': 2020, 'source_url': 'https://jntua.ac.in/r20-syllabus'})
        r23_jntua, _ = Regulation.objects.get_or_create(name='R23', university=jntua, defaults={'effective_from_year': 2023, 'source_url': 'https://jntua.ac.in/r23-syllabus'})
        r20_jntuk, _ = Regulation.objects.get_or_create(name='R20', university=jntuk, defaults={'effective_from_year': 2020, 'source_url': 'https://jntuk.edu.in/r20-syllabus'})
        r23_jntuk, _ = Regulation.objects.get_or_create(name='R23', university=jntuk, defaults={'effective_from_year': 2023, 'source_url': 'https://jntuk.edu.in/r23-syllabus'})

        self.stdout.write("-> Regulations seeded.")

        # 5. Curriculum & Subjects Sample
        curriculum_cse, _ = Curriculum.objects.get_or_create(
            college=colleges_dict['JNTUACEA'],
            branch=branches_dict['CSE'],
            regulation=r23_jntua,
            admission_year=2023,
            defaults={
                'university': jntua,
                'program': btech,
                'name': 'JNTUA R23 B.Tech CSE Curriculum',
                'source_type': Curriculum.SourceType.OFFICIAL_UNIVERSITY,
                'source_url': 'https://jntua.ac.in/r23-cse-syllabus.pdf',
                'verified_at': timezone.now()
            }
        )

        subjects_data = [
            {'semester': 1, 'subject_code': '23A05101', 'subject_name': 'Linear Algebra and Calculus', 'credits': 3.0},
            {'semester': 1, 'subject_code': '23A05102', 'subject_name': 'Communicative English', 'credits': 2.0},
            {'semester': 1, 'subject_code': '23A05103', 'subject_name': 'Programming in C', 'credits': 3.0},
            {'semester': 2, 'subject_code': '23A05201', 'subject_name': 'Differential Equations & Vector Calculus', 'credits': 3.0},
            {'semester': 2, 'subject_code': '23A05202', 'subject_name': 'Data Structures', 'credits': 3.0},
            {'semester': 3, 'subject_code': '23A05301', 'subject_name': 'Discrete Mathematics', 'credits': 3.0},
            {'semester': 3, 'subject_code': '23A05302', 'subject_name': 'Object Oriented Programming through Java', 'credits': 3.0},
            {'semester': 3, 'subject_code': '23A05303', 'subject_name': 'Database Management Systems', 'credits': 3.0},
            {'semester': 4, 'subject_code': '23A05401', 'subject_name': 'Probability and Statistics', 'credits': 3.0},
            {'semester': 4, 'subject_code': '23A05402', 'subject_name': 'Operating Systems', 'credits': 3.0},
            {'semester': 4, 'subject_code': '23A05403', 'subject_name': 'Computer Networks', 'credits': 3.0},
            {'semester': 4, 'subject_code': '23A05404', 'subject_name': 'Python Programming & Data Analysis', 'credits': 3.0},
            {'semester': 5, 'subject_code': '23A05501', 'subject_name': 'Design and Analysis of Algorithms', 'credits': 3.0},
            {'semester': 5, 'subject_code': '23A05502', 'subject_name': 'Software Engineering', 'credits': 3.0},
            {'semester': 5, 'subject_code': '23A05503', 'subject_name': 'Machine Learning', 'credits': 3.0},
        ]
        for sdata in subjects_data:
            Subject.objects.get_or_create(curriculum=curriculum_cse, subject_code=sdata['subject_code'], defaults=sdata)

        self.stdout.write("-> Curriculum and subjects seeded.")

        # 6. Skills
        skills_data = [
            ('Python', 'python', Skill.Category.PROGRAMMING, 'High-level programming language for AI, Data Science & Web'),
            ('Java', 'java', Skill.Category.PROGRAMMING, 'Object-oriented language for enterprise & Android'),
            ('C++', 'cpp', Skill.Category.PROGRAMMING, 'Systems programming and competitive coding'),
            ('C', 'c', Skill.Category.PROGRAMMING, 'Procedural programming foundation'),
            ('JavaScript', 'javascript', Skill.Category.WEB, 'Web scripting language'),
            ('TypeScript', 'typescript', Skill.Category.WEB, 'Typed superset of JavaScript'),
            ('HTML/CSS', 'html-css', Skill.Category.WEB, 'Markup and styling for web pages'),
            ('React', 'react', Skill.Category.WEB, 'Frontend UI framework'),
            ('Node.js', 'nodejs', Skill.Category.WEB, 'Server-side JavaScript runtime'),
            ('Django', 'django', Skill.Category.WEB, 'Python web framework'),
            ('SQL', 'sql', Skill.Category.DATABASE, 'Relational database querying'),
            ('PostgreSQL', 'postgresql', Skill.Category.DATABASE, 'Advanced open-source relational database'),
            ('MongoDB', 'mongodb', Skill.Category.DATABASE, 'NoSQL document database'),
            ('Statistics & Probability', 'statistics', Skill.Category.MATHEMATICS, 'Statistical analysis & hypothesis testing'),
            ('Linear Algebra', 'linear-algebra', Skill.Category.MATHEMATICS, 'Matrix operations & vector spaces'),
            ('Data Analysis', 'data-analysis', Skill.Category.AI, 'Exploratory data analysis with Pandas & NumPy'),
            ('Machine Learning', 'machine-learning', Skill.Category.AI, 'Supervised & unsupervised predictive algorithms'),
            ('Deep Learning', 'deep-learning', Skill.Category.AI, 'Neural networks, PyTorch & TensorFlow'),
            ('Natural Language Processing', 'nlp', Skill.Category.AI, 'Text processing, LLMs & Transformers'),
            ('Computer Vision', 'computer-vision', Skill.Category.AI, 'Image recognition & OpenCV'),
            ('Generative AI', 'generative-ai', Skill.Category.AI, 'LLMs, RAG, Prompt Engineering'),
            ('Git & GitHub', 'git', Skill.Category.INFRASTRUCTURE, 'Version control and collaboration'),
            ('Docker', 'docker', Skill.Category.INFRASTRUCTURE, 'Containerization technology'),
            ('Kubernetes', 'kubernetes', Skill.Category.INFRASTRUCTURE, 'Container orchestration'),
            ('AWS', 'aws', Skill.Category.INFRASTRUCTURE, 'Amazon Web Services Cloud'),
            ('Linux', 'linux', Skill.Category.INFRASTRUCTURE, 'Linux operating system administration'),
            ('Cyber Security', 'cyber-security', Skill.Category.INFRASTRUCTURE, 'Ethical hacking & network defense'),
            ('Embedded Systems', 'embedded-systems', Skill.Category.HARDWARE, 'Microcontrollers, Arduino, ARM'),
            ('IoT', 'iot', Skill.Category.HARDWARE, 'Internet of Things sensor networks'),
            ('Communication Skills', 'communication', Skill.Category.SOFT_SKILLS, 'Verbal & written technical communication'),
            ('Aptitude & Reasoning', 'aptitude', Skill.Category.SOFT_SKILLS, 'Quantitative aptitude for campus placements'),
        ]

        skills_dict = {}
        for name, slug, cat, desc in skills_data:
            s_obj, _ = Skill.objects.get_or_create(name=name, defaults={'slug': slug, 'category': cat, 'description': desc})
            skills_dict[slug] = s_obj

        self.stdout.write("-> Skills seeded.")

        # 7. Interests
        interests_data = [
            ('Artificial Intelligence', 'artificial-intelligence', 'Machine Learning, Neural Nets & GenAI'),
            ('Data Science', 'data-science', 'Big Data Analytics & Visualization'),
            ('Web Development', 'web-development', 'Full-stack web applications'),
            ('Mobile Development', 'mobile-development', 'Android & iOS apps'),
            ('Cyber Security', 'cyber-security', 'Ethical hacking & Security engineering'),
            ('Cloud Computing', 'cloud-computing', 'AWS, Azure & DevOps'),
            ('Robotics & Embedded Systems', 'robotics-embedded', 'Hardware & Autonomous Systems'),
            ('Competitive Programming', 'competitive-programming', 'Algorithms & Data Structures'),
        ]
        interests_dict = {}
        for name, slug, desc in interests_data:
            i_obj, _ = Interest.objects.get_or_create(name=name, defaults={'slug': slug, 'description': desc})
            interests_dict[slug] = i_obj

        self.stdout.write("-> Interests seeded.")

        # 8. Careers & CareerSkills
        careers_data = [
            ('AI Engineer', 'ai-engineer', 'Specializes in developing machine learning models and GenAI applications.', 'AI & Tech'),
            ('Data Scientist', 'data-scientist', 'Extracts actionable insights from data using statistical models.', 'Data & Analytics'),
            ('Full-Stack Developer', 'full-stack-developer', 'Builds complete end-to-end web applications.', 'Software Engineering'),
            ('Backend Developer', 'backend-developer', 'Builds scalable server APIs and databases.', 'Software Engineering'),
            ('Cloud & DevOps Engineer', 'cloud-devops-engineer', 'Automates cloud infrastructure deployment.', 'Cloud & Infrastructure'),
            ('Cyber Security Engineer', 'cyber-security-engineer', 'Protects systems from cyber threats.', 'Security'),
            ('Embedded Systems Engineer', 'embedded-systems-engineer', 'Develops firmware for IoT & electronics.', 'Hardware'),
        ]

        careers_dict = {}
        for name, slug, desc, ind in careers_data:
            c_obj, _ = Career.objects.get_or_create(name=name, defaults={'slug': slug, 'description': desc, 'industry': ind})
            careers_dict[slug] = c_obj

        # Career Skill mappings
        ai_eng_skills = [
            (skills_dict['python'], 4, 1.0, True),
            (skills_dict['statistics'], 3, 1.0, True),
            (skills_dict['machine-learning'], 4, 1.0, True),
            (skills_dict['deep-learning'], 3, 0.9, True),
            (skills_dict['generative-ai'], 3, 0.8, False),
            (skills_dict['sql'], 2, 0.7, False),
        ]
        for sk, req_lvl, imp, req in ai_eng_skills:
            CareerSkill.objects.get_or_create(career=careers_dict['ai-engineer'], skill=sk, defaults={'required_level': req_lvl, 'importance': imp, 'required': req})

        fullstack_skills = [
            (skills_dict['javascript'], 4, 1.0, True),
            (skills_dict['react'], 3, 1.0, True),
            (skills_dict['html-css'], 4, 0.9, True),
            (skills_dict['python'], 3, 0.8, False),
            (skills_dict['django'], 3, 0.9, False),
            (skills_dict['sql'], 3, 0.9, True),
            (skills_dict['git'], 3, 0.8, True),
        ]
        for sk, req_lvl, imp, req in fullstack_skills:
            CareerSkill.objects.get_or_create(career=careers_dict['full-stack-developer'], skill=sk, defaults={'required_level': req_lvl, 'importance': imp, 'required': req})

        self.stdout.write("-> Careers & Career Skills seeded.")

        # 9. Course Providers & Categories
        nptel, _ = CourseProvider.objects.get_or_create(name='NPTEL / SWAYAM', defaults={'provider_type': CourseProvider.ProviderType.GOVT_MOOC, 'website': 'https://nptel.ac.in'})
        coursera, _ = CourseProvider.objects.get_or_create(name='Coursera', defaults={'provider_type': CourseProvider.ProviderType.GLOBAL_MOOC, 'website': 'https://coursera.org'})
        udemy, _ = CourseProvider.objects.get_or_create(name='Udemy', defaults={'provider_type': CourseProvider.ProviderType.GLOBAL_MOOC, 'website': 'https://udemy.com'})
        youtube, _ = CourseProvider.objects.get_or_create(name='YouTube Education', defaults={'provider_type': CourseProvider.ProviderType.OPEN_SOURCE, 'website': 'https://youtube.com'})
        google_dev, _ = CourseProvider.objects.get_or_create(name='Google Cloud', defaults={'provider_type': CourseProvider.ProviderType.INDUSTRY, 'website': 'https://cloud.google.com/training'})

        cat_ai, _ = CourseCategory.objects.get_or_create(name='Artificial Intelligence & Machine Learning', defaults={'slug': 'ai-ml'})
        cat_web, _ = CourseCategory.objects.get_or_create(name='Web Development', defaults={'slug': 'web-dev'})
        cat_data, _ = CourseCategory.objects.get_or_create(name='Data Science & Analytics', defaults={'slug': 'data-science'})
        cat_core, _ = CourseCategory.objects.get_or_create(name='Core Computer Science', defaults={'slug': 'core-cs'})

        self.stdout.write("-> Course Providers & Categories seeded.")

        # 10. Courses
        courses_data = [
            {
                'slug': 'nptel-python-for-data-science',
                'title': 'Python for Data Science (NPTEL)',
                'provider': nptel,
                'category': cat_data,
                'description': 'Comprehensive NPTEL course covering Python fundamentals, NumPy, Pandas, and exploratory data analysis.',
                'url': 'https://onlinecourses.nptel.ac.in/noc24_cs54/preview',
                'difficulty': Course.Difficulty.BEGINNER,
                'duration_hours': 30,
                'cost_type': Course.CostType.FREE,
                'rating': 4.7,
                'skills_taught': [skills_dict['python'], skills_dict['data-analysis']],
                'skills_required': [],
                'careers': [careers_dict['ai-engineer'], careers_dict['data-scientist']],
                'interests': [interests_dict['artificial-intelligence'], interests_dict['data-science']]
            },
            {
                'slug': 'nptel-introduction-to-machine-learning',
                'title': 'Introduction to Machine Learning (NPTEL / IIT Kharagpur)',
                'provider': nptel,
                'category': cat_ai,
                'description': 'Standard 12-week IIT NPTEL course covering linear regression, classification, decision trees, SVM, and clustering.',
                'url': 'https://onlinecourses.nptel.ac.in/noc24_cs55/preview',
                'difficulty': Course.Difficulty.INTERMEDIATE,
                'duration_hours': 45,
                'cost_type': Course.CostType.FREE,
                'rating': 4.8,
                'skills_taught': [skills_dict['machine-learning'], skills_dict['statistics']],
                'skills_required': [(skills_dict['python'], 2), (skills_dict['statistics'], 2)],
                'careers': [careers_dict['ai-engineer'], careers_dict['data-scientist']],
                'interests': [interests_dict['artificial-intelligence']]
            },
            {
                'slug': 'deep-learning-specialization-coursera',
                'title': 'Deep Learning Specialization (DeepLearning.AI)',
                'provider': coursera,
                'category': cat_ai,
                'description': 'Master Deep Learning, Convolutional Networks (CNNs), RNNs, Transformers, and PyTorch.',
                'url': 'https://coursera.org/specializations/deep-learning',
                'difficulty': Course.Difficulty.ADVANCED,
                'duration_hours': 60,
                'cost_type': Course.CostType.FREEMIUM,
                'rating': 4.9,
                'skills_taught': [skills_dict['deep-learning'], skills_dict['nlp'], skills_dict['computer-vision']],
                'skills_required': [(skills_dict['python'], 3), (skills_dict['machine-learning'], 3)],
                'careers': [careers_dict['ai-engineer']],
                'interests': [interests_dict['artificial-intelligence']]
            },
            {
                'slug': 'full-stack-web-development-react-django',
                'title': 'Full-Stack Web Development with React and Django',
                'provider': udemy,
                'category': cat_web,
                'description': 'Build modern responsive full-stack applications with React frontend and Django REST Framework backend.',
                'url': 'https://udemy.com/course/full-stack-django-react',
                'difficulty': Course.Difficulty.INTERMEDIATE,
                'duration_hours': 40,
                'cost_type': Course.CostType.PAID,
                'rating': 4.6,
                'skills_taught': [skills_dict['react'], skills_dict['django'], skills_dict['sql'], skills_dict['javascript']],
                'skills_required': [(skills_dict['html-css'], 2), (skills_dict['javascript'], 2)],
                'careers': [careers_dict['full-stack-developer'], careers_dict['backend-developer']],
                'interests': [interests_dict['web-development']]
            },
            {
                'slug': 'nptel-database-management-systems',
                'title': 'Database Management Systems (NPTEL / IIT Madras)',
                'provider': nptel,
                'category': cat_core,
                'description': 'Relational algebra, SQL, ER modeling, normalization, transaction processing, and indexing.',
                'url': 'https://onlinecourses.nptel.ac.in/noc24_cs56/preview',
                'difficulty': Course.Difficulty.BEGINNER,
                'duration_hours': 35,
                'cost_type': Course.CostType.FREE,
                'rating': 4.5,
                'skills_taught': [skills_dict['sql'], skills_dict['postgresql']],
                'skills_required': [],
                'careers': [careers_dict['backend-developer'], careers_dict['full-stack-developer'], careers_dict['data-scientist']],
                'interests': [interests_dict['web-development'], interests_dict['data-science']]
            }
        ]

        course_objects_dict = {}
        for cdata in courses_data:
            course_obj, _ = Course.objects.get_or_create(
                slug=cdata['slug'],
                defaults={
                    'title': cdata['title'],
                    'provider': cdata['provider'],
                    'category': cdata['category'],
                    'description': cdata['description'],
                    'url': cdata['url'],
                    'difficulty': cdata['difficulty'],
                    'duration_hours': cdata['duration_hours'],
                    'cost_type': cdata['cost_type'],
                    'rating': cdata['rating'],
                    'source_type': Course.SourceType.VERIFIED_OFFICIAL,
                    'last_verified_at': timezone.now()
                }
            )
            course_objects_dict[cdata['slug']] = course_obj

            # Skills taught
            for sk in cdata['skills_taught']:
                CourseSkill.objects.get_or_create(course=course_obj, skill=sk, skill_type='TAUGHT', defaults={'target_level': 3})

            # Skills required
            for sk, min_lvl in cdata['skills_required']:
                CourseSkill.objects.get_or_create(course=course_obj, skill=sk, skill_type='REQUIRED', defaults={'target_level': min_lvl})
                CoursePrerequisite.objects.get_or_create(course=course_obj, required_skill=sk, defaults={'minimum_skill_level': min_lvl, 'required': True})

            # Careers
            for car in cdata['careers']:
                CourseCareer.objects.get_or_create(course=course_obj, career=car)

            # Interests
            for intr in cdata['interests']:
                CourseInterest.objects.get_or_create(course=course_obj, interest=intr)

            # Target CSE Branch
            CourseBranch.objects.get_or_create(course=course_obj, branch=branches_dict['CSE'])

        # Course to Course prerequisite link: Deep Learning requires ML
        ml_course = course_objects_dict['nptel-introduction-to-machine-learning']
        dl_course = course_objects_dict['deep-learning-specialization-coursera']
        CoursePrerequisite.objects.get_or_create(course=dl_course, prerequisite_course=ml_course, defaults={'required': True})

        self.stdout.write("-> Courses & Prerequisites seeded.")

        # 11. Skill Assessment & MCQ Questions
        python_quiz, _ = Assessment.objects.get_or_create(
            title='Python Programming Proficiency Assessment',
            skill=skills_dict['python'],
            defaults={
                'description': 'Assess your Python programming knowledge from basic syntax to object-oriented programming and Pandas.',
                'difficulty': Assessment.Difficulty.INTERMEDIATE,
                'duration_minutes': 15,
                'passing_score': 60.0
            }
        )

        q1, _ = Question.objects.get_or_create(
            assessment=python_quiz,
            question_text='Which data structure in Python is immutable?',
            defaults={'question_type': Question.QuestionType.MCQ, 'difficulty': Assessment.Difficulty.BEGINNER, 'marks': 1, 'explanation': 'Tuples are immutable sequences in Python.'}
        )
        Option.objects.get_or_create(question=q1, option_text='List', defaults={'is_correct': False})
        Option.objects.get_or_create(question=q1, option_text='Dictionary', defaults={'is_correct': False})
        Option.objects.get_or_create(question=q1, option_text='Tuple', defaults={'is_correct': True})
        Option.objects.get_or_create(question=q1, option_text='Set', defaults={'is_correct': False})

        q2, _ = Question.objects.get_or_create(
            assessment=python_quiz,
            question_text='What is the output of len({"a": 1, "b": 2, "a": 3}) in Python?',
            defaults={'question_type': Question.QuestionType.MCQ, 'difficulty': Assessment.Difficulty.INTERMEDIATE, 'marks': 1, 'explanation': 'Dictionary keys are unique. The duplicate key "a" overwrites the value, resulting in length 2.'}
        )
        Option.objects.get_or_create(question=q2, option_text='3', defaults={'is_correct': False})
        Option.objects.get_or_create(question=q2, option_text='2', defaults={'is_correct': True})
        Option.objects.get_or_create(question=q2, option_text='1', defaults={'is_correct': False})
        Option.objects.get_or_create(question=q2, option_text='Error', defaults={'is_correct': False})

        self.stdout.write("-> Skill Assessment & Questions seeded.")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))

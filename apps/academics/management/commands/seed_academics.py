from django.core.management.base import BaseCommand
from apps.academics.models import University, College, Branch, Regulation, Semester, Subject, BranchSubject

class Command(BaseCommand):
    help = "Seed initial academic hierarchy data (Universities, Colleges, Branches, Regulations, Semesters, Subjects)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Academic Hierarchy...")

        # 1. Universities
        jntuh, _ = University.objects.get_or_create(
            code="JNTUH",
            defaults={"name": "Jawaharlal Nehru Technological University Hyderabad", "website": "https://jntuh.ac.in"}
        )
        anna, _ = University.objects.get_or_create(
            code="ANNA",
            defaults={"name": "Anna University", "website": "https://annauniv.edu"}
        )

        # 2. Colleges
        cbit, _ = College.objects.get_or_create(
            code="CBIT",
            defaults={"name": "Chaitanya Bharathi Institute of Technology", "university": jntuh, "location": "Hyderabad"}
        )
        vniti, _ = College.objects.get_or_create(
            code="VNIT",
            defaults={"name": "VNR Vignana Jyothi Institute of Engineering and Technology", "university": jntuh, "location": "Hyderabad"}
        )

        # 3. Branches
        branches_data = [
            ("CSE", "Computer Science and Engineering"),
            ("AI_DS", "Artificial Intelligence and Data Science"),
            ("ECE", "Electronics and Communication Engineering"),
            ("EEE", "Electrical and Electronics Engineering"),
            ("MECH", "Mechanical Engineering"),
            ("CIVIL", "Civil Engineering"),
        ]
        branch_objs = {}
        for code, name in branches_data:
            b, _ = Branch.objects.get_or_create(code=code, defaults={"name": name})
            branch_objs[code] = b

        # 4. Regulations
        r20, _ = Regulation.objects.get_or_create(
            name="R20",
            university=jntuh,
            defaults={"description": "Academic Regulation 2020", "start_year": 2020, "end_year": 2023, "is_active": True}
        )
        r23, _ = Regulation.objects.get_or_create(
            name="R23",
            university=jntuh,
            defaults={"description": "Academic Regulation 2023", "start_year": 2023, "is_active": True}
        )

        # 5. Semesters
        sem_objs = {}
        for num in range(1, 9):
            sem, _ = Semester.objects.get_or_create(number=num, defaults={"name": f"Semester {num}"})
            sem_objs[num] = sem

        # 6. Core Engineering Subjects
        subjects_data = [
            ("CS101", "Data Structures and Algorithms", "Pointers, Trees, Graphs, Sorting, Searching", 4.0),
            ("CS102", "Database Management Systems", "Relational Algebra, SQL, Indexing, Transactions", 3.0),
            ("CS103", "Operating Systems", "Processes, Threads, Memory Management, File Systems", 3.0),
            ("CS104", "Computer Networks", "OSI Model, TCP/IP, Routing, Sockets", 3.0),
            ("AI101", "Introduction to Machine Learning", "Supervised, Unsupervised, Regression, Classification", 4.0),
            ("AI102", "Deep Learning and Neural Networks", "CNNs, RNNs, Transformers, PyTorch/TensorFlow", 4.0),
            ("EC101", "Digital Signal Processing", "Signals, Systems, Fourier Transforms, Filters", 3.0),
            ("EC102", "Microcontrollers and Embedded Systems", "ARM, AVR, I2C, SPI, Real-time Systems", 3.0),
            ("MA101", "Linear Algebra and Differential Equations", "Matrices, Eigenvalues, ODEs, Vector Calculus", 4.0),
            ("MA102", "Probability and Statistics", "Random Variables, Distributions, Hypothesis Testing", 3.0),
        ]

        subject_objs = {}
        for code, title, desc, creds in subjects_data:
            s, _ = Subject.objects.get_or_create(
                code=code,
                defaults={"name": title, "description": desc, "credits": creds}
            )
            subject_objs[code] = s

        # 7. Map BranchSubjects
        maps = [
            (branch_objs["CSE"], r20, sem_objs[3], subject_objs["CS101"], False),
            (branch_objs["CSE"], r20, sem_objs[4], subject_objs["CS102"], False),
            (branch_objs["CSE"], r20, sem_objs[5], subject_objs["CS103"], False),
            (branch_objs["CSE"], r20, sem_objs[6], subject_objs["CS104"], False),
            (branch_objs["AI_DS"], r23, sem_objs[3], subject_objs["CS101"], False),
            (branch_objs["AI_DS"], r23, sem_objs[4], subject_objs["AI101"], False),
            (branch_objs["AI_DS"], r23, sem_objs[5], subject_objs["AI102"], True),
            (branch_objs["ECE"], r20, sem_objs[4], subject_objs["EC101"], False),
            (branch_objs["ECE"], r20, sem_objs[5], subject_objs["EC102"], False),
        ]

        for branch, reg, sem, subj, is_elec in maps:
            BranchSubject.objects.get_or_create(
                branch=branch,
                regulation=reg,
                semester=sem,
                subject=subj,
                defaults={"is_elective": is_elec}
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Academic Hierarchy data!"))

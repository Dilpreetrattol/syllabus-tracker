import os
from app import create_app, db


def main(seed=False):
    app = create_app()
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        print('Tables created.')

        if seed:
            from app.models import User, Department, Course, Subject, Topic, Enrollment, AcademicYear
            print('Seeding test data...')
            
            # Admin user
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    name='Admin',
                    email='admin@example.com',
                    role='hod',
                    department='CSE',
                    phone='1234567890',
                    profile_image='admin.png',
                    is_active=True
                )
                admin.set_password('ChangeMe123!')
                db.session.add(admin)
                db.session.commit()
                print('Admin user created: admin@example.com')

            # Department
            dept = Department.query.filter_by(name='CSE').first()
            if not dept:
                dept = Department(
                    name='CSE',
                    code='CSE',
                    hod_id=admin.id,
                    description='Computer Science and Engineering'
                )
                db.session.add(dept)
                db.session.commit()
                print('Department created: CSE')

            # Academic Year
            year = AcademicYear.query.filter_by(year='2025-2026').first()
            if not year:
                year = AcademicYear(
                    year='2025-2026',
                    is_current=True,
                    start_date='2025-07-01',
                    end_date='2026-06-30'
                )
                db.session.add(year)
                db.session.commit()
                print('Academic year created: 2025-2026')

            # Course
            course = Course.query.filter_by(code='BTECHCSE').first()
            if not course:
                course = Course(
                    name='B.Tech CSE',
                    code='BTECHCSE',
                    department_id=dept.id,
                    total_semesters=8,
                    description='B.Tech in Computer Science'
                )
                db.session.add(course)
                db.session.commit()
                print('Course created: B.Tech CSE')

            # Subject
            subject = Subject.query.filter_by(code='CS101').first()
            if not subject:
                subject = Subject(
                    name='Data Structures',
                    code='CS101',
                    course_id=course.id,
                    semester=3,
                    credits=4,
                    description='Core Data Structures',
                    teacher_id=admin.id,
                    academic_year_id=year.id,
                    syllabus_document='syllabus_cs101.pdf',
                    total_hours=48,
                    is_active=True
                )
                db.session.add(subject)
                db.session.commit()
                print('Subject created: Data Structures')

            # Topic
            existing_topics = subject.topics.count()
            if existing_topics < 6:
                # Seed a richer ordered topic list if not already present
                topic_specs = [
                    (1, 'Introduction to Data Structures', 'Overview & complexity basics', 4),
                    (2, 'Arrays and Strings', 'Static & dynamic arrays, string ops', 6),
                    (3, 'Linked Lists', 'Singly, doubly, circular lists', 6),
                    (4, 'Stacks and Queues', 'ADT, array & linked implementations', 6),
                    (5, 'Trees', 'Binary, BST operations, traversal', 8),
                    (6, 'Hash Tables', 'Hash functions, collision strategies', 6),
                    (7, 'Heaps & Priority Queues', 'Binary heap operations', 6),
                    (8, 'Graphs', 'Representation, BFS/DFS fundamentals', 10),
                ]
                for order, name, desc, hours in topic_specs:
                    if not Topic.query.filter_by(subject_id=subject.id, order=order).first():
                        t = Topic(
                            subject_id=subject.id,
                            name=name,
                            description=desc,
                            order=order,
                            hours_allocated=hours,
                            expected_date=None,
                            completed_date=None,
                            is_completed=False,
                            completion_notes='',
                            attachments=None,
                            prerequisites=None
                        )
                        db.session.add(t)
                db.session.commit()
                print(f'Seeded topics for {subject.code} (count now: {subject.topics.count()})')

            # Student user
            student = User.query.filter_by(email='student1@example.com').first()
            if not student:
                student = User(
                    name='Student One',
                    email='student1@example.com',
                    role='student',
                    department='CSE',
                    phone='9876543210',
                    profile_image='student1.png',
                    is_active=True
                )
                student.set_password('Student123!')
                db.session.add(student)
                db.session.commit()
                print('Student user created: student1@example.com')

            # Enrollment
            enrollment = Enrollment.query.filter_by(student_id=student.id, subject_id=subject.id).first()
            if not enrollment:
                enrollment = Enrollment(
                    student_id=student.id,
                    subject_id=subject.id,
                    status='active',
                    progress=0.0
                )
                db.session.add(enrollment)
                db.session.commit()
                print('Enrollment created for student1@example.com in Data Structures')

            # Additional subject (Algorithms) with topics
            subject2 = Subject.query.filter_by(code='CS102').first()
            if not subject2:
                subject2 = Subject(
                    name='Algorithms',
                    code='CS102',
                    course_id=course.id,
                    semester=3,
                    credits=4,
                    description='Algorithm design and analysis',
                    teacher_id=admin.id,
                    academic_year_id=year.id,
                    syllabus_document='syllabus_cs102.pdf',
                    total_hours=54,
                    is_active=True
                )
                db.session.add(subject2)
                db.session.commit()
                print('Subject created: Algorithms')

            if subject2.topics.count() < 6:
                algo_topics = [
                    (1, 'Complexity Analysis', 'Big-O, Omega, Theta notation', 4),
                    (2, 'Recursion & Backtracking', 'Recursive patterns & backtracking', 6),
                    (3, 'Divide and Conquer', 'Merge sort, quick sort paradigms', 6),
                    (4, 'Greedy Algorithms', 'Greedy choice property examples', 6),
                    (5, 'Dynamic Programming', 'Memoization & tabulation', 8),
                    (6, 'Graph Algorithms', 'Shortest paths & MST basics', 10),
                ]
                for order, name, desc, hours in algo_topics:
                    if not Topic.query.filter_by(subject_id=subject2.id, order=order).first():
                        t = Topic(
                            subject_id=subject2.id,
                            name=name,
                            description=desc,
                            order=order,
                            hours_allocated=hours,
                            expected_date=None,
                            completed_date=None,
                            is_completed=False,
                            completion_notes='',
                            attachments=None,
                            prerequisites=None
                        )
                        db.session.add(t)
                db.session.commit()
                print(f'Seeded topics for {subject2.code} (count now: {subject2.topics.count()})')

            # Enroll student in Algorithms as well
            enrollment2 = Enrollment.query.filter_by(student_id=student.id, subject_id=subject2.id).first()
            if not enrollment2:
                enrollment2 = Enrollment(
                    student_id=student.id,
                    subject_id=subject2.id,
                    status='active',
                    progress=0.0
                )
                db.session.add(enrollment2)
                db.session.commit()
                print('Enrollment created for student1@example.com in Algorithms')


if __name__ == '__main__':
    seed_flag = os.environ.get('SEED', '0') == '1'
    main(seed=seed_flag)

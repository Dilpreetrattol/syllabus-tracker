"""
Comprehensive data seeding script for syllabus tracker
Creates departments, faculty, students, subjects, topics, and enrollments
"""
import sys
from datetime import datetime, date, timedelta

from app import create_app, db
from app.models import (
    User, Department, Course, Subject, Topic, 
    Enrollment, AcademicYear
)


def seed_all():
    app = create_app()
    with app.app_context():
        print("Starting comprehensive data seeding...")
        
        # Create Academic Year
        print("\n1. Creating Academic Year...")
        academic_year = AcademicYear.query.filter_by(year='2024-2025').first()
        if not academic_year:
            academic_year = AcademicYear(
                year='2024-2025',
                start_date=date(2024, 8, 1),
                end_date=date(2025, 5, 31),
                is_current=True
            )
            db.session.add(academic_year)
            db.session.commit()
            print(f"   ✓ Created academic year: {academic_year.year}")
        else:
            print(f"   ✓ Academic year already exists: {academic_year.year}")
        
        # Create Departments
        print("\n2. Creating Departments...")
        departments_data = [
            {'name': 'Computer Science', 'code': 'CSE', 'description': 'Computer Science and Engineering'},
            {'name': 'Electronics', 'code': 'ECE', 'description': 'Electronics and Communication Engineering'},
            {'name': 'Mechanical', 'code': 'MECH', 'description': 'Mechanical Engineering'},
            {'name': 'Information Technology', 'code': 'IT', 'description': 'Information Technology'},
        ]
        
        departments = {}
        for dept_data in departments_data:
            dept = Department.query.filter_by(code=dept_data['code']).first()
            if not dept:
                dept = Department(**dept_data)
                db.session.add(dept)
                db.session.commit()
                print(f"   ✓ Created department: {dept.name} ({dept.code})")
            else:
                print(f"   ✓ Department already exists: {dept.name} ({dept.code})")
            departments[dept.code] = dept
        
        # Create Courses
        print("\n3. Creating Courses...")
        courses_data = [
            {'name': 'B.Tech Computer Science', 'code': 'BTCS', 'department_id': departments['CSE'].id, 'total_semesters': 8},
            {'name': 'B.Tech Electronics', 'code': 'BTEC', 'department_id': departments['ECE'].id, 'total_semesters': 8},
            {'name': 'B.Tech Mechanical', 'code': 'BTME', 'department_id': departments['MECH'].id, 'total_semesters': 8},
            {'name': 'B.Tech Information Technology', 'code': 'BTIT', 'department_id': departments['IT'].id, 'total_semesters': 8},
        ]
        
        courses = {}
        for course_data in courses_data:
            course = Course.query.filter_by(code=course_data['code']).first()
            if not course:
                course = Course(**course_data)
                db.session.add(course)
                db.session.commit()
                print(f"   ✓ Created course: {course.name}")
            else:
                print(f"   ✓ Course already exists: {course.name}")
            courses[course.code] = course
        
        # Create Faculty (Teachers and HODs)
        print("\n4. Creating Faculty Members...")
        faculty_data = [
            # CSE Department
            {'name': 'Dr. Sarah Johnson', 'email': 'sarah.johnson@university.edu', 'role': 'hod', 'department': 'CSE', 'phone': '1234567890'},
            {'name': 'Prof. Michael Chen', 'email': 'michael.chen@university.edu', 'role': 'teacher', 'department': 'CSE', 'phone': '1234567891'},
            {'name': 'Dr. Emily Rodriguez', 'email': 'emily.rodriguez@university.edu', 'role': 'teacher', 'department': 'CSE', 'phone': '1234567892'},
            {'name': 'Prof. David Kumar', 'email': 'david.kumar@university.edu', 'role': 'teacher', 'department': 'CSE', 'phone': '1234567893'},
            
            # ECE Department
            {'name': 'Dr. Robert Williams', 'email': 'robert.williams@university.edu', 'role': 'hod', 'department': 'ECE', 'phone': '1234567894'},
            {'name': 'Prof. Lisa Anderson', 'email': 'lisa.anderson@university.edu', 'role': 'teacher', 'department': 'ECE', 'phone': '1234567895'},
            {'name': 'Dr. James Taylor', 'email': 'james.taylor@university.edu', 'role': 'teacher', 'department': 'ECE', 'phone': '1234567896'},
            
            # MECH Department
            {'name': 'Dr. Patricia Brown', 'email': 'patricia.brown@university.edu', 'role': 'hod', 'department': 'MECH', 'phone': '1234567897'},
            {'name': 'Prof. Thomas Wilson', 'email': 'thomas.wilson@university.edu', 'role': 'teacher', 'department': 'MECH', 'phone': '1234567898'},
            
            # IT Department
            {'name': 'Dr. Jennifer Davis', 'email': 'jennifer.davis@university.edu', 'role': 'hod', 'department': 'IT', 'phone': '1234567899'},
            {'name': 'Prof. Christopher Lee', 'email': 'christopher.lee@university.edu', 'role': 'teacher', 'department': 'IT', 'phone': '1234567800'},
        ]
        
        faculty = {}
        for fac_data in faculty_data:
            user = User.query.filter_by(email=fac_data['email']).first()
            if not user:
                user = User(**fac_data, is_active=True)
                user.set_password('teacher123')
                db.session.add(user)
                db.session.commit()
                print(f"   ✓ Created {fac_data['role']}: {user.name} ({user.email})")
            else:
                print(f"   ✓ Faculty already exists: {user.name}")
            faculty[user.email] = user
        
        # Update department HODs
        for dept_code, dept in departments.items():
            hod = User.query.filter_by(department=dept_code, role='hod').first()
            if hod and dept.hod_id != hod.id:
                dept.hod_id = hod.id
                db.session.commit()
                print(f"   ✓ Assigned HOD for {dept.name}: {hod.name}")
        
        # Create Students
        print("\n5. Creating Students...")
        students_data = [
            # CSE Students
            {'name': 'Alice Thompson', 'email': 'alice.thompson@student.edu', 'department': 'CSE', 'phone': '9876543210'},
            {'name': 'Bob Martinez', 'email': 'bob.martinez@student.edu', 'department': 'CSE', 'phone': '9876543211'},
            {'name': 'Charlie Garcia', 'email': 'charlie.garcia@student.edu', 'department': 'CSE', 'phone': '9876543212'},
            {'name': 'Diana Robinson', 'email': 'diana.robinson@student.edu', 'department': 'CSE', 'phone': '9876543213'},
            {'name': 'Ethan Clark', 'email': 'ethan.clark@student.edu', 'department': 'CSE', 'phone': '9876543214'},
            
            # ECE Students
            {'name': 'Fiona Lewis', 'email': 'fiona.lewis@student.edu', 'department': 'ECE', 'phone': '9876543215'},
            {'name': 'George Walker', 'email': 'george.walker@student.edu', 'department': 'ECE', 'phone': '9876543216'},
            {'name': 'Hannah Hall', 'email': 'hannah.hall@student.edu', 'department': 'ECE', 'phone': '9876543217'},
            
            # MECH Students
            {'name': 'Ian Young', 'email': 'ian.young@student.edu', 'department': 'MECH', 'phone': '9876543218'},
            {'name': 'Julia King', 'email': 'julia.king@student.edu', 'department': 'MECH', 'phone': '9876543219'},
            
            # IT Students
            {'name': 'Kevin Wright', 'email': 'kevin.wright@student.edu', 'department': 'IT', 'phone': '9876543220'},
            {'name': 'Laura Scott', 'email': 'laura.scott@student.edu', 'department': 'IT', 'phone': '9876543221'},
            {'name': 'Mike Green', 'email': 'mike.green@student.edu', 'department': 'IT', 'phone': '9876543222'},
        ]
        
        students = {}
        for stud_data in students_data:
            user = User.query.filter_by(email=stud_data['email']).first()
            if not user:
                user = User(**stud_data, role='student', is_active=True)
                user.set_password('student123')
                db.session.add(user)
                db.session.commit()
                print(f"   ✓ Created student: {user.name} ({user.email})")
            else:
                print(f"   ✓ Student already exists: {user.name}")
            students[user.email] = user
        
        # Create Subjects
        print("\n6. Creating Subjects...")
        subjects_data = [
            # CSE Subjects
            {'name': 'Data Structures', 'code': 'CS201', 'teacher': 'michael.chen@university.edu', 'department': 'CSE', 
             'semester': 3, 'credits': 4, 'total_hours': 60, 'description': 'Fundamental data structures and algorithms'},
            {'name': 'Database Management Systems', 'code': 'CS301', 'teacher': 'emily.rodriguez@university.edu', 'department': 'CSE',
             'semester': 5, 'credits': 4, 'total_hours': 60, 'description': 'Design and implementation of database systems'},
            {'name': 'Operating Systems', 'code': 'CS302', 'teacher': 'david.kumar@university.edu', 'department': 'CSE',
             'semester': 5, 'credits': 4, 'total_hours': 60, 'description': 'Operating system concepts and design'},
            
            # ECE Subjects
            {'name': 'Digital Electronics', 'code': 'EC201', 'teacher': 'lisa.anderson@university.edu', 'department': 'ECE',
             'semester': 3, 'credits': 4, 'total_hours': 60, 'description': 'Digital circuits and logic design'},
            {'name': 'Microprocessors', 'code': 'EC301', 'teacher': 'james.taylor@university.edu', 'department': 'ECE',
             'semester': 5, 'credits': 4, 'total_hours': 60, 'description': 'Microprocessor architecture and programming'},
            
            # MECH Subjects
            {'name': 'Thermodynamics', 'code': 'ME201', 'teacher': 'thomas.wilson@university.edu', 'department': 'MECH',
             'semester': 3, 'credits': 4, 'total_hours': 60, 'description': 'Laws of thermodynamics and applications'},
            
            # IT Subjects
            {'name': 'Web Development', 'code': 'IT201', 'teacher': 'christopher.lee@university.edu', 'department': 'IT',
             'semester': 3, 'credits': 4, 'total_hours': 60, 'description': 'Modern web development technologies'},
        ]
        
        subjects = {}
        for subj_data in subjects_data:
            teacher_email = subj_data.pop('teacher')
            dept_code = subj_data.pop('department')
            
            subject = Subject.query.filter_by(code=subj_data['code']).first()
            if not subject:
                teacher = faculty[teacher_email]
                course = courses[f"BT{dept_code[:2].upper()}"]
                
                subject = Subject(
                    **subj_data,
                    teacher_id=teacher.id,
                    course_id=course.id,
                    academic_year_id=academic_year.id,
                    is_active=True
                )
                db.session.add(subject)
                db.session.commit()
                print(f"   ✓ Created subject: {subject.name} ({subject.code}) - Teacher: {teacher.name}")
            else:
                print(f"   ✓ Subject already exists: {subject.name}")
            subjects[subject.code] = subject
        
        # Create Topics for each subject
        print("\n7. Creating Topics for Subjects...")
        topics_templates = {
            'CS201': [
                {'name': 'Introduction to Data Structures', 'order': 1, 'hours_allocated': 6, 'is_completed': True},
                {'name': 'Arrays and Linked Lists', 'order': 2, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Stacks and Queues', 'order': 3, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Trees and Binary Trees', 'order': 4, 'hours_allocated': 10, 'is_completed': True},
                {'name': 'Graphs and Graph Algorithms', 'order': 5, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'Sorting Algorithms', 'order': 6, 'hours_allocated': 8, 'is_completed': False},
                {'name': 'Searching Algorithms', 'order': 7, 'hours_allocated': 6, 'is_completed': False},
                {'name': 'Hashing', 'order': 8, 'hours_allocated': 4, 'is_completed': False},
            ],
            'CS301': [
                {'name': 'Database Fundamentals', 'order': 1, 'hours_allocated': 6, 'is_completed': True},
                {'name': 'ER Modeling', 'order': 2, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Relational Model', 'order': 3, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'SQL Basics', 'order': 4, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'Advanced SQL', 'order': 5, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'Normalization', 'order': 6, 'hours_allocated': 8, 'is_completed': False},
                {'name': 'Transaction Management', 'order': 7, 'hours_allocated': 6, 'is_completed': False},
                {'name': 'Concurrency Control', 'order': 8, 'hours_allocated': 4, 'is_completed': False},
            ],
            'CS302': [
                {'name': 'OS Introduction', 'order': 1, 'hours_allocated': 6, 'is_completed': True},
                {'name': 'Process Management', 'order': 2, 'hours_allocated': 10, 'is_completed': True},
                {'name': 'CPU Scheduling', 'order': 3, 'hours_allocated': 8, 'is_completed': False},
                {'name': 'Memory Management', 'order': 4, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'File Systems', 'order': 5, 'hours_allocated': 8, 'is_completed': False},
            ],
            'EC201': [
                {'name': 'Number Systems', 'order': 1, 'hours_allocated': 6, 'is_completed': True},
                {'name': 'Boolean Algebra', 'order': 2, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Logic Gates', 'order': 3, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Combinational Circuits', 'order': 4, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'Sequential Circuits', 'order': 5, 'hours_allocated': 10, 'is_completed': False},
            ],
            'EC301': [
                {'name': '8086 Architecture', 'order': 1, 'hours_allocated': 8, 'is_completed': True},
                {'name': 'Assembly Language', 'order': 2, 'hours_allocated': 10, 'is_completed': False},
                {'name': 'Memory Interface', 'order': 3, 'hours_allocated': 8, 'is_completed': False},
            ],
            'ME201': [
                {'name': 'Basic Concepts', 'order': 1, 'hours_allocated': 6, 'is_completed': True},
                {'name': 'First Law of Thermodynamics', 'order': 2, 'hours_allocated': 10, 'is_completed': True},
                {'name': 'Second Law of Thermodynamics', 'order': 3, 'hours_allocated': 10, 'is_completed': False},
            ],
            'IT201': [
                {'name': 'HTML & CSS', 'order': 1, 'hours_allocated': 10, 'is_completed': True},
                {'name': 'JavaScript Basics', 'order': 2, 'hours_allocated': 10, 'is_completed': True},
                {'name': 'React Framework', 'order': 3, 'hours_allocated': 12, 'is_completed': False},
                {'name': 'Backend with Node.js', 'order': 4, 'hours_allocated': 12, 'is_completed': False},
            ],
        }
        
        for subject_code, topics_data in topics_templates.items():
            subject = subjects[subject_code]
            for topic_data in topics_data:
                topic = Topic.query.filter_by(subject_id=subject.id, order=topic_data['order']).first()
                if not topic:
                    topic = Topic(**topic_data, subject_id=subject.id)
                    db.session.add(topic)
                    db.session.commit()
            print(f"   ✓ Created {len(topics_data)} topics for {subject.name}")
        
        # Create Enrollments
        print("\n8. Creating Student Enrollments...")
        enrollment_mapping = [
            # CSE Students enrolled in CSE subjects
            ('alice.thompson@student.edu', ['CS201', 'CS301', 'CS302']),
            ('bob.martinez@student.edu', ['CS201', 'CS301']),
            ('charlie.garcia@student.edu', ['CS201', 'CS302']),
            ('diana.robinson@student.edu', ['CS301', 'CS302']),
            ('ethan.clark@student.edu', ['CS201']),
            
            # ECE Students
            ('fiona.lewis@student.edu', ['EC201', 'EC301']),
            ('george.walker@student.edu', ['EC201']),
            ('hannah.hall@student.edu', ['EC201', 'EC301']),
            
            # MECH Students
            ('ian.young@student.edu', ['ME201']),
            ('julia.king@student.edu', ['ME201']),
            
            # IT Students
            ('kevin.wright@student.edu', ['IT201']),
            ('laura.scott@student.edu', ['IT201']),
            ('mike.green@student.edu', ['IT201']),
        ]
        
        enrollment_count = 0
        for student_email, subject_codes in enrollment_mapping:
            student = students[student_email]
            for subject_code in subject_codes:
                subject = subjects[subject_code]
                
                enrollment = Enrollment.query.filter_by(
                    student_id=student.id,
                    subject_id=subject.id
                ).first()
                
                if not enrollment:
                    enrollment = Enrollment(
                        student_id=student.id,
                        subject_id=subject.id,
                        status='active',
                        progress=0.0
                    )
                    db.session.add(enrollment)
                    enrollment_count += 1
        
        db.session.commit()
        print(f"   ✓ Created {enrollment_count} new enrollments")
        
        # Print Summary
        print("\n" + "="*60)
        print("DATA SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Departments: {Department.query.count()}")
        print(f"   • Courses: {Course.query.count()}")
        print(f"   • Faculty (Teachers + HODs): {User.query.filter(User.role.in_(['teacher', 'hod'])).count()}")
        print(f"   • Students: {User.query.filter_by(role='student').count()}")
        print(f"   • Subjects: {Subject.query.count()}")
        print(f"   • Topics: {Topic.query.count()}")
        print(f"   • Enrollments: {Enrollment.query.count()}")
        
        print(f"\n🔐 Login Credentials:")
        print(f"   Coordinator: coordinator@university.edu / coord123")
        print(f"   Any HOD: [email]@university.edu / teacher123")
        print(f"   Any Teacher: [email]@university.edu / teacher123")
        print(f"   Any Student: [email]@student.edu / student123")
        print(f"\n   Examples:")
        print(f"   • alice.thompson@student.edu / student123")
        print(f"   • michael.chen@university.edu / teacher123")
        print(f"   • sarah.johnson@university.edu / teacher123 (CSE HOD)")
        print("="*60)
        
        return 0


if __name__ == '__main__':
    raise SystemExit(seed_all())

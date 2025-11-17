from app import create_app, db
from app.models import User, Subject, Department

app = create_app()
with app.app_context():
    # Check HOD
    hod = User.query.filter_by(email='sarah.johnson@university.edu').first()
    if hod:
        print(f'HOD: {hod.name}, Dept: {hod.department}, Role: {hod.role}')
        
        # Check teachers
        teachers = User.query.filter_by(department='CSE', role='teacher', is_active=True).all()
        print(f'\nTeachers in CSE: {len(teachers)}')
        for t in teachers:
            subjects = t.subjects_teaching.filter_by(is_active=True).all()
            print(f'  - {t.name}: {len(subjects)} subjects')
            for s in subjects:
                print(f'    * {s.name} ({s.code})')
        
        # Check department
        dept = Department.query.filter_by(code='CSE').first()
        if dept:
            print(f'\nDepartment: {dept.name} ({dept.code})')
            print(f'HOD ID in dept: {dept.hod_id}')
    else:
        print('HOD not found')

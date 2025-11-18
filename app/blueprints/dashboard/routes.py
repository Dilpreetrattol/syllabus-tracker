from flask import render_template, request, url_for, current_app
from flask_login import login_required
from app.blueprints.auth.decorators import role_required
from . import dashboard_bp


@dashboard_bp.route('/student')
@login_required
@role_required('student')
def student():
    from app.models import Enrollment, Subject
    from app.services.progress import subject_progress
    from flask_login import current_user
    from datetime import datetime
    
    enrollments = current_user.enrollments.join(Subject, Enrollment.subject_id == Subject.id).all()

    # Build subject progress list
    subject_data = []
    total_progress = 0
    for e in enrollments:
        subj = e.subject
        progress = subject_progress(subj)
        subject_data.append({
            'subject': subj,
            'progress_percent': progress
        })
        total_progress += progress

    average_progress = round(total_progress / len(subject_data), 1) if subject_data else 0
    subject_preview = subject_data[:3]
    current_date = datetime.utcnow().strftime('%B %d, %Y')

    return render_template('dashboard/student.html', enrollments=enrollments, subject_preview=subject_preview, average_progress=average_progress, current_date=current_date)


@dashboard_bp.route('/teacher')
@login_required
@role_required('teacher')
def teacher():
    from app.models import Subject, Topic, Enrollment
    from flask_login import current_user
    from sqlalchemy import func
    from datetime import datetime
    from app import db
    
    # Get subjects taught by the teacher with topic stats
    subjects = current_user.subjects_teaching.filter_by(is_active=True).all()

    subject_rows = []
    total_progress_accum = 0
    pending_updates = 0
    for subject in subjects:
        total_topics = subject.topics.count()
        completed_topics = subject.topics.filter_by(is_completed=True).count()
        progress = (completed_topics / total_topics * 100) if total_topics else 0
        enroll_count = Enrollment.query.filter_by(subject_id=subject.id).count()
        if total_topics - completed_topics > 0:
            pending_updates += 1
        subject_rows.append({
            'subject': subject,
            'code': subject.code,
            'name': subject.name,
            'enrolled': enroll_count,
            'progress_percent': round(progress,1)
        })
        total_progress_accum += progress

    metrics = {
        'total_assigned': len(subjects),
        'avg_progress': round(total_progress_accum / len(subjects),1) if subjects else 0,
        'pending_updates': pending_updates,
        'date': datetime.utcnow().strftime('%B %d, %Y')
    }

    return render_template('dashboard/teacher.html', metrics=metrics, subject_rows=subject_rows)

@dashboard_bp.route('/teacher/subject/<int:subject_id>')
@login_required
@role_required('teacher')
def teacher_subject(subject_id):
    from app.models import Subject, Topic, Enrollment, User
    from flask_login import current_user
    from datetime import datetime
    try:
        # Ensure subject belongs to teacher
        subject = Subject.query.get_or_404(subject_id)
        if subject.teacher_id != current_user.id:
            return render_template('dashboard/teacher_subject.html', error='Unauthorized access.'), 403

        topics = subject.topics.order_by(Topic.order.asc()).all()
        total = len(topics)
        completed = sum(1 for t in topics if t.is_completed)
        progress_percent = round(completed / total * 100, 1) if total else 0
        enroll_q = Enrollment.query.filter_by(subject_id=subject.id)
        enroll_count = enroll_q.count()
        enrollments = enroll_q.all()
        return render_template(
            'dashboard/teacher_subject.html',
            subject=subject,
            topics=topics,
            progress_percent=progress_percent,
            enroll_count=enroll_count,
            enrollments=enrollments,
        )
    except Exception as e:
        return render_template('dashboard/teacher_subject.html', error=f'Error loading subject: {str(e)}'), 500

@dashboard_bp.route('/teacher/topic/<int:topic_id>/cover', methods=['POST'])
@login_required
@role_required('teacher')
def teacher_mark_topic(topic_id):
    from app.models import Topic, Subject
    from flask_login import current_user
    from app import db
    topic = Topic.query.get_or_404(topic_id)
    subject = topic.subject
    if subject.teacher_id != current_user.id:
        return {'status': 'error', 'message': 'Unauthorized'}, 403
    if not topic.is_completed:
        topic.is_completed = True
        db.session.commit()
    return {'status': 'ok', 'completed': topic.is_completed}


@dashboard_bp.route('/hod')
@login_required
@role_required('hod')
def hod():
    from app.models import User, Subject, Enrollment, Topic, Department
    from flask_login import current_user
    from sqlalchemy import func
    from app import db
    
    # Get HOD's department
    department = Department.query.filter_by(code=current_user.department).first()
    
    # Count faculty in department
    faculty_count = User.query.filter_by(
        department=current_user.department,
        role='teacher',
        is_active=True
    ).count()
    
    # Get subjects in department (via teachers)
    dept_teachers = User.query.filter_by(
        department=current_user.department,
        role='teacher',
        is_active=True
    ).all()
    teacher_ids = [t.id for t in dept_teachers]
    
    subjects = Subject.query.filter(
        Subject.teacher_id.in_(teacher_ids),
        Subject.is_active == True
    ).all() if teacher_ids else []
    
    # Count students enrolled in department subjects
    subject_ids = [s.id for s in subjects]
    student_count = db.session.query(func.count(func.distinct(Enrollment.student_id))).filter(
        Enrollment.subject_id.in_(subject_ids)
    ).scalar() if subject_ids else 0
    
    # Calculate average progress across all department subjects
    total_topics = 0
    completed_topics = 0
    for subject in subjects:
        total_topics += subject.topics.count()
        completed_topics += subject.topics.filter_by(is_completed=True).count()
    
    avg_progress = round((completed_topics / total_topics * 100), 1) if total_topics > 0 else 0
    
    # Get faculty with their subject stats
    faculty_data = []
    for teacher in dept_teachers:
        teacher_subjects = [s for s in subjects if s.teacher_id == teacher.id]
        subject_ids_teacher = [s.id for s in teacher_subjects]
        student_count_teacher = db.session.query(func.count(func.distinct(Enrollment.student_id))).filter(
            Enrollment.subject_id.in_(subject_ids_teacher)
        ).scalar() if subject_ids_teacher else 0
        
        faculty_data.append({
            'teacher': teacher,
            'subject_count': len(teacher_subjects),
            'student_count': student_count_teacher
        })
    
    return render_template('dashboard/hod.html',
                          department=department,
                          faculty_count=faculty_count,
                          subject_count=len(subjects),
                          student_count=student_count,
                          avg_progress=avg_progress,
                          faculty_data=faculty_data)


@dashboard_bp.route('/coordinator')
@login_required
@role_required('coordinator')
def coordinator():
    from app.models import User, Subject, Enrollment, Department
    from sqlalchemy import func
    from flask_login import current_user
    from app import db

    departments = Department.query.all()
    total_users = User.query.filter_by(is_active=True).count()
    active_subjects = Subject.query.filter_by(is_active=True).count()

    # Unassigned teachers = teachers with no active subject
    teachers = User.query.filter_by(role='teacher', is_active=True).all()
    teacher_ids_with_subjects = set([s.teacher_id for s in Subject.query.filter_by(is_active=True).all() if s.teacher_id])
    unassigned_teachers = sum(1 for t in teachers if t.id not in teacher_ids_with_subjects)

    # Recent activity (if model exists)
    recent_activity = []
    try:
        from app.models import ActivityLog
        recent_activity = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()
    except Exception:
        pass

    metrics = {
        'total_users': total_users,
        'active_subjects': active_subjects,
        'unassigned_teachers': unassigned_teachers
    }

    return render_template('dashboard/coordinator.html', metrics=metrics, recent_activity=recent_activity, active_section='dashboard')



@dashboard_bp.route('/coordinator/users')
@login_required
@role_required('coordinator')
def coordinator_users():
    from app.models import User
    users = User.query.order_by(User.name.asc()).all()
    return render_template('coordinator/users.html', users=users, active_section='users')

# Create user (AJAX)
@dashboard_bp.route('/coordinator/users/create', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_create_user():
    from app.models import User
    from app import db
    import json, secrets
    data = (json.loads(request.data) if request.is_json else request.form)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    role = data.get('role', '').strip()
    department = data.get('department', '').strip() or None
    password = data.get('password') or ("Init-" + secrets.token_hex(4))
    if not name or not email or not role:
        return {'status':'error','message':'Name, email and role are required.'}, 400
    # Check email uniqueness
    if User.query.filter_by(email=email).first():
        return {'status':'error','message':'Email already exists.'}, 400
    u = User(name=name, email=email, role=role, department=department, is_active=True)
    u.set_password(password)
    try:
        db.session.add(u)
        db.session.commit()
        # Send invite/reset email if email config allows
        try:
            from itsdangerous import URLSafeTimedSerializer
            from app.services.email import send_email
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps({'email': u.email}, salt='password-reset')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            current_app.logger.info(f"Invite/reset link for {u.email}: {reset_url}")
            send_email(
                to_email=u.email,
                subject="Welcome to Syllabus Tracker",
                body_text=f"Hello {u.name},\n\nYour account has been created. Set your password here: {reset_url}\nThe link expires in 1 hour.",
                body_html=f"""
                    <p>Hello {u.name},</p>
                    <p>Your account has been created. <a href='{reset_url}'>Click here to set your password</a>.</p>
                    <p>This link expires in 1 hour.</p>
                """
            )
        except Exception:
            pass
        return {'status':'ok','user':{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'role': u.role,
            'department': u.department
        }}
    except Exception as e:
        db.session.rollback()
        return {'status':'error','message': str(e)}, 400

# Edit user (AJAX)
@dashboard_bp.route('/coordinator/users/<int:user_id>/edit', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_edit_user(user_id):
    from app.models import User
    from app import db
    import json
    data = (json.loads(request.data) if request.is_json else request.form)
    user = User.query.get_or_404(user_id)
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.department = data.get('department', user.department)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}, 400
    return {'status': 'ok', 'user': {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'department': user.department
    }}

# Delete user (AJAX)
@dashboard_bp.route('/coordinator/users/<int:user_id>/delete', methods=['DELETE'])
@login_required
@role_required('coordinator')
def coordinator_delete_user(user_id):
    from app.models import User
    from app import db
    user = User.query.get_or_404(user_id)
    try:
        user.is_active = False
        db.session.commit()
        return {'status': 'ok', 'deactivated': user_id}
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}, 400

# Restore user (AJAX)
@dashboard_bp.route('/coordinator/users/<int:user_id>/restore', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_restore_user(user_id):
    from app.models import User
    from app import db
    user = User.query.get_or_404(user_id)
    try:
        user.is_active = True
        db.session.commit()
        return {'status': 'ok', 'restored': user_id}
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'message': str(e)}, 400


@dashboard_bp.route('/coordinator/subjects')
@login_required
@role_required('coordinator')
def coordinator_subjects():
    from app.models import Subject, User
    subjects = Subject.query.filter_by(is_active=True).order_by(Subject.code.asc()).all()
    teachers = User.query.filter_by(role='teacher', is_active=True).order_by(User.name.asc()).all()
    return render_template('coordinator/subjects.html', subjects=subjects, teachers=teachers, active_section='subjects')


@dashboard_bp.route('/coordinator/enrollments')
@login_required
@role_required('coordinator')
def coordinator_enrollments():
    from app.models import Subject
    subjects = Subject.query.filter_by(is_active=True).order_by(Subject.code.asc()).all()
    return render_template('coordinator/enrollments.html', subjects=subjects, active_section='enrollments')

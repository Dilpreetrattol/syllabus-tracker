from flask import render_template
from flask_login import login_required
from app.blueprints.auth.decorators import role_required
from . import dashboard_bp


@dashboard_bp.route('/student')
@login_required
@role_required('student')
def student():
    from app.models import Enrollment, Subject
    from flask_login import current_user
    enrollments = (
        current_user.enrollments
        .join(Subject, Enrollment.subject_id == Subject.id)
        .all()
    )
    return render_template('dashboard/student.html', enrollments=enrollments)


@dashboard_bp.route('/teacher')
@login_required
@role_required('teacher')
def teacher():
    from app.models import Subject, Topic
    from flask_login import current_user
    from sqlalchemy import func
    
    # Get subjects taught by the teacher with topic stats
    subjects = current_user.subjects_teaching.filter_by(is_active=True).all()
    
    subject_data = []
    for subject in subjects:
        total_topics = subject.topics.count()
        completed_topics = subject.topics.filter_by(is_completed=True).count()
        progress = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        subject_data.append({
            'subject': subject,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'progress': round(progress, 1)
        })
    
    return render_template('dashboard/teacher.html', subject_data=subject_data)


@dashboard_bp.route('/hod')
@login_required
@role_required('hod')
def hod():
    return render_template('dashboard/hod.html')


@dashboard_bp.route('/coordinator')
@login_required
@role_required('coordinator')
def coordinator():
    return render_template('dashboard/coordinator.html')

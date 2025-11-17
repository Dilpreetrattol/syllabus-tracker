from flask import render_template, abort
from flask_login import login_required, current_user
from app.blueprints.auth.decorators import role_required
from . import student_bp
from app.models import Enrollment, Subject, Topic, User
from app.services.progress import subject_progress, topics_progress
from app import db
from sqlalchemy import func

@student_bp.route('/subjects')
@login_required
@role_required('student')
def subjects():
    # Fetch enrollments with related subjects efficiently
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    listing = []
    for e in enrollments:
        subj = e.subject
        teacher = User.query.get(subj.teacher_id)
        progress = subject_progress(subj)
        listing.append({
            'subject': subj,
            'teacher': teacher,
            'progress_percent': progress
        })
    return render_template('student/subjects.html', subjects=listing, active_section='subjects')

@student_bp.route('/subject/<int:subject_id>')
@login_required
@role_required('student')
def subject_detail(subject_id):
    try:
        # Verify enrollment access
        enrollment = Enrollment.query.filter_by(student_id=current_user.id, subject_id=subject_id).first()
        if not enrollment:
            abort(404)

        subject = Subject.query.get_or_404(subject_id)
        topics = subject.topics.order_by(Topic.order.asc()).all()

        progress_percent = topics_progress(topics)

        # Sample learn list (placeholder) could be derived from topics types later
        learn_items = [t.name for t in topics[:4]]

        teacher = User.query.get(subject.teacher_id)
        instructors = [
            {'name': teacher.name if teacher else 'Unknown', 'role': 'Professor'},
        ]

        return render_template(
            'student/subject_detail.html',
            subject=subject,
            topics=topics,
            enrollment=enrollment,
            progress_percent=progress_percent,
            learn_items=learn_items,
            instructors=instructors,
            active_section='subjects'
        )
    except Exception as e:
        from flask import flash, redirect, url_for
        flash(f'Error loading subject details', 'error')
        return redirect(url_for('student.subjects'))

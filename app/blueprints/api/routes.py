from flask import jsonify, request, make_response
from flask_login import login_required
from app.blueprints.auth.decorators import role_required
from . import api_bp
from app import db



@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@api_bp.route('/coordinator/subjects', methods=['GET'])
@login_required
@role_required('coordinator')
def coordinator_list_subjects():
    from app.models import Subject, User
    subjects = Subject.query.order_by(Subject.code.asc()).all()
    data = []
    for s in subjects:
        data.append({
            'id': s.id,
            'name': s.name,
            'code': s.code,
            'teacher_id': s.teacher_id,
            'teacher_name': s.teacher.name if s.teacher_id else None,
            'is_active': s.is_active
        })
    return jsonify({'subjects': data})


@api_bp.route('/coordinator/subjects', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_create_subject():
    from app.models import Subject, User
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    code = (payload.get('code') or '').strip()
    teacher_id = payload.get('teacher_id')
    credits = payload.get('credits')

    if not name or not code or not teacher_id:
        return jsonify({'error': 'Missing required fields: name, code, teacher_id'}), 400

    teacher = User.query.get(teacher_id)
    if not teacher or teacher.role != 'teacher':
        return jsonify({'error': 'Invalid teacher_id'}), 400

    subject = Subject(name=name, code=code, teacher_id=teacher.id)
    if isinstance(credits, int):
        subject.credits = credits

    db.session.add(subject)
    db.session.commit()

    return jsonify({'id': subject.id, 'name': subject.name, 'code': subject.code}), 201


@api_bp.route('/coordinator/subjects/<int:subject_id>/topics', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_add_topic(subject_id):
    from app.models import Subject, Topic
    from datetime import datetime
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    expected_date = payload.get('expected_date')
    if not name:
        return jsonify({'error': 'Missing topic name'}), 400

    subject = Subject.query.get_or_404(subject_id)
    # Determine next order
    last = subject.topics.order_by(Topic.order.desc()).first()
    next_order = (last.order + 1) if last else 1

    topic = Topic(subject_id=subject.id, name=name, order=next_order)
    if expected_date:
        try:
            topic.expected_date = datetime.strptime(expected_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'expected_date must be YYYY-MM-DD'}), 400

    db.session.add(topic)
    db.session.commit()

    return jsonify({'id': topic.id, 'name': topic.name, 'order': topic.order}), 201


@api_bp.route('/coordinator/subjects/<int:subject_id>/topics', methods=['GET'])
@login_required
@role_required('coordinator')
def coordinator_list_topics(subject_id):
    from app.models import Subject, Topic
    subject = Subject.query.get_or_404(subject_id)
    topics = subject.topics.order_by(Topic.order.asc()).all()
    return jsonify({
        'subject': {
            'id': subject.id,
            'name': subject.name,
            'code': subject.code
        },
        'topics': [
            {
                'id': t.id,
                'name': t.name,
                'order': t.order,
                'is_completed': t.is_completed,
                'expected_date': t.expected_date.isoformat() if t.expected_date else None
            }
            for t in topics
        ]
    })


@api_bp.route('/coordinator/topics/<int:topic_id>', methods=['DELETE'])
@login_required
@role_required('coordinator')
def coordinator_delete_topic(topic_id):
    from app.models import Topic
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return jsonify({'status': 'deleted'})


@api_bp.route('/coordinator/topics/<int:topic_id>', methods=['PATCH'])
@login_required
@role_required('coordinator')
def coordinator_update_topic(topic_id):
    from app.models import Topic
    from datetime import datetime
    topic = Topic.query.get_or_404(topic_id)
    payload = request.get_json(silent=True) or {}
    name = payload.get('name')
    expected_date = payload.get('expected_date')
    if name is not None:
        name = name.strip()
        if not name:
            return jsonify({'error':'name cannot be empty'}), 400
        topic.name = name
    if expected_date is not None:
        if expected_date == '':
            topic.expected_date = None
        else:
            try:
                topic.expected_date = datetime.strptime(expected_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'expected_date must be YYYY-MM-DD'}), 400
    db.session.commit()
    return jsonify({'id': topic.id, 'name': topic.name, 'expected_date': topic.expected_date.isoformat() if topic.expected_date else None})


@api_bp.route('/coordinator/subjects/<int:subject_id>/topics/reorder', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_reorder_topics(subject_id):
    from app.models import Subject, Topic
    payload = request.get_json(silent=True) or {}
    order_list = payload.get('order')
    if not isinstance(order_list, list) or not all(isinstance(i, int) for i in order_list):
        return jsonify({'error': 'order must be a list of topic ids'}), 400
    subject = Subject.query.get_or_404(subject_id)
    # Fetch topics for subject to validate and update
    topics = {t.id: t for t in subject.topics.all()}
    if set(order_list) != set(topics.keys()):
        return jsonify({'error': 'order list must match exactly the subject\'s topic ids'}), 400
    for idx, tid in enumerate(order_list, start=1):
        topics[tid].order = idx
    db.session.commit()
    return jsonify({'status': 'ok'})


@api_bp.route('/coordinator/subjects/<int:subject_id>/enrollments', methods=['GET'])
@login_required
@role_required('coordinator')
def coordinator_list_enrollments(subject_id):
    from app.models import Subject, Enrollment, User
    Subject.query.get_or_404(subject_id)
    rows = (
        db.session.query(Enrollment, User)
        .join(User, Enrollment.student_id == User.id)
        .filter(Enrollment.subject_id == subject_id)
        .order_by(User.name.asc())
        .all()
    )
    data = [
        {
            'student_id': u.id,
            'name': u.name,
            'email': u.email,
            'status': e.status,
            'enrolled_at': e.enrolled_at.isoformat(),
        }
        for e, u in rows
    ]
    return jsonify({'enrollments': data})


@api_bp.route('/coordinator/subjects/<int:subject_id>/enrollments', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_add_enrollment(subject_id):
    from app.models import Subject, Enrollment, User
    Subject.query.get_or_404(subject_id)
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    if not email:
        return jsonify({'error':'email required'}), 400
    user = User.query.filter_by(email=email, is_active=True).first()
    if not user or user.role != 'student':
        return jsonify({'error':'student not found'}), 404
    existing = Enrollment.query.filter_by(subject_id=subject_id, student_id=user.id).first()
    if existing:
        return jsonify({'status':'exists'}), 200
    db.session.add(Enrollment(subject_id=subject_id, student_id=user.id))
    db.session.commit()
    return jsonify({'status':'added', 'student_id': user.id})


@api_bp.route('/coordinator/subjects/<int:subject_id>/enrollments/upload', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_upload_enrollments(subject_id):
    from app.models import Subject, Enrollment, User
    import csv, io
    Subject.query.get_or_404(subject_id)
    f = request.files.get('file')
    if not f:
        return jsonify({'error':'file required'}), 400
    content = f.read().decode('utf-8', errors='ignore')
    reader = csv.reader(io.StringIO(content))
    added = 0
    skipped = 0
    for row in reader:
        if not row:
            continue
        email = row[0].strip().lower()
        if not email:
            continue
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user or user.role != 'student':
            skipped += 1
            continue
        exists = Enrollment.query.filter_by(subject_id=subject_id, student_id=user.id).first()
        if exists:
            skipped += 1
            continue
        db.session.add(Enrollment(subject_id=subject_id, student_id=user.id))
        added += 1
    db.session.commit()
    return jsonify({'status':'ok', 'added': added, 'skipped': skipped})


@api_bp.route('/coordinator/subjects/<int:subject_id>/enrollments/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('coordinator')
def coordinator_delete_enrollment(subject_id, student_id):
    from app.models import Enrollment
    e = Enrollment.query.filter_by(subject_id=subject_id, student_id=student_id).first_or_404()
    db.session.delete(e)
    db.session.commit()
    return jsonify({'status':'deleted'})


@api_bp.route('/coordinator/users', methods=['POST'])
@login_required
@role_required('coordinator')
def coordinator_create_user():
    from app.models import User
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    email = (payload.get('email') or '').strip().lower()
    department = (payload.get('department') or '').strip() or None
    role = (payload.get('role') or 'student').strip().lower()
    if not name or not email:
        return jsonify({'error':'name and email required'}), 400
    if role not in ('student','teacher','hod','coordinator','admin'):
        return jsonify({'error':'invalid role'}), 400
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error':'email already exists'}), 409
    user = User(name=name, email=email, role=role, department=department, is_active=True)
    # Set a temporary password; in production change flow to invite/reset
    user.set_password('changeme123')
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}), 201


@api_bp.route('/coordinator/enrollments/template', methods=['GET'])
@login_required
@role_required('coordinator')
def coordinator_enrollment_template():
    content = 'email\nstudent1@example.com\nstudent2@example.com\n'
    resp = make_response(content)
    resp.headers['Content-Type'] = 'text/csv'
    resp.headers['Content-Disposition'] = 'attachment; filename="enrollments_template.csv"'
    return resp

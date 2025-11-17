from datetime import datetime
from app import db

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    code = db.Column(db.String(20))
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester = db.Column(db.Integer)
    credits = db.Column(db.Integer)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_year.id'))
    syllabus_document = db.Column(db.String(256))
    total_hours = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    topics = db.relationship('Topic', backref='subject', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='subject', lazy='dynamic', cascade='all, delete-orphan')

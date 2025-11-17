from datetime import datetime
from app import db

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    hours_allocated = db.Column(db.Integer)
    expected_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    is_completed = db.Column(db.Boolean, default=False)
    completion_notes = db.Column(db.Text)
    attachments = db.Column(db.JSON)
    prerequisites = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

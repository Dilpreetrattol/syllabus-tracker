from datetime import datetime
from app import db

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    resource_type = db.Column(db.String(20))  # pdf, video, link, etc.
    url = db.Column(db.String(512))
    file_path = db.Column(db.String(512))
    description = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

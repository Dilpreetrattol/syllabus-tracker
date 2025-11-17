from datetime import datetime
from app import db

class ReportCache(db.Model):
    __tablename__ = 'report_cache'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(64), nullable=False)
    filters = db.Column(db.JSON)
    data = db.Column(db.JSON)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

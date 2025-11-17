from datetime import datetime
from app import db

class AcademicYear(db.Model):
    __tablename__ = 'academic_year'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(9), unique=True, nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

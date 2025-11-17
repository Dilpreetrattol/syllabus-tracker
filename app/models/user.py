from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))  # Fixed: increased from 128 to 255
    role = db.Column(db.String(20), nullable=False)  # student, teacher, hod, coordinator
    department = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    user_metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subjects_teaching = db.relationship('Subject', backref='teacher', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

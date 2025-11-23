#!/usr/bin/env python3
"""
Database initialization script for production deployment
Run this after deployment to set up the database schema
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def init_db():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # Import all models to ensure they're registered
        from app.models import (
            user, subject, topic, enrollment, 
            topic_progress, academic_year, course, 
            department, activity_log, notification,
            comment, resource, report_cache
        )
        
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default admin user if none exists
            from app.models.user import User
            admin = User.query.filter_by(role='admin').first()
            if not admin:
                admin_user = User(
                    email='admin@example.com',
                    name='System Administrator',
                    role='admin',
                    department='Administration'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Default admin user created (admin@example.com / admin123)")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
            
    return True

if __name__ == '__main__':
    success = init_db()
    sys.exit(0 if success else 1)
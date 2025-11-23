#!/usr/bin/env python3
"""
Create default test users for the syllabus tracker application
This script creates users for all roles so you can test the different portals
"""

from app import create_app, db
from app.models.user import User

def create_test_users():
    """Create default test users for all roles"""
    
    app = create_app()
    with app.app_context():
        # Create users for each role
        users_to_create = [
            {
                'name': 'Admin User',
                'email': 'admin@college.edu',
                'password': 'Admin123!',
                'role': 'hod',
                'department': 'CSE'
            },
            {
                'name': 'John Teacher',
                'email': 'teacher@college.edu', 
                'password': 'Teacher123!',
                'role': 'teacher',
                'department': 'CSE'
            },
            {
                'name': 'Mary Coordinator',
                'email': 'coordinator@college.edu',
                'password': 'Coordinator123!', 
                'role': 'coordinator',
                'department': 'CSE'
            },
            {
                'name': 'Alice Student',
                'email': 'student@college.edu',
                'password': 'Student123!',
                'role': 'student', 
                'department': 'CSE'
            }
        ]
        
        print("🚀 Creating default test users...")
        print("=" * 50)
        
        for user_data in users_to_create:
            # Check if user already exists
            existing = User.query.filter_by(email=user_data['email']).first()
            if existing:
                print(f"✅ User already exists: {existing.email} ({existing.role})")
                continue
                
            # Create new user
            user = User(
                name=user_data['name'],
                email=user_data['email'], 
                role=user_data['role'],
                department=user_data['department'],
                user_metadata={'created_by': 'setup_script'}
            )
            user.set_password(user_data['password'])
            
            db.session.add(user)
            print(f"✨ Created: {user_data['email']} ({user_data['role']})")
        
        db.session.commit()
        print("=" * 50)
        print("🎉 User creation complete!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        
        for user_data in users_to_create:
            print(f"🔑 {user_data['role'].upper()} Portal:")
            print(f"   Email: {user_data['email']}")
            print(f"   Password: {user_data['password']}")
            print()

if __name__ == '__main__':
    create_test_users()
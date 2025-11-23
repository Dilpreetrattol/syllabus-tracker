from app import create_app

app = create_app()

# Auto-create database tables on startup (for Railway deployment)
def init_db():
    try:
        from app import db
        from app.models.user import User
        
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create default users if they don't exist
            default_users = [
                {'name': 'Admin User', 'email': 'admin@college.edu', 'password': 'Admin123!', 'role': 'hod', 'department': 'CSE'},
                {'name': 'Test Teacher', 'email': 'teacher@college.edu', 'password': 'Teacher123!', 'role': 'teacher', 'department': 'CSE'},
                {'name': 'Test Coordinator', 'email': 'coordinator@college.edu', 'password': 'Coordinator123!', 'role': 'coordinator', 'department': 'CSE'},
                {'name': 'Test Student', 'email': 'student@college.edu', 'password': 'Student123!', 'role': 'student', 'department': 'CSE'}
            ]
            
            for user_data in default_users:
                existing = User.query.filter_by(email=user_data['email']).first()
                if not existing:
                    user = User(
                        name=user_data['name'],
                        email=user_data['email'],
                        role=user_data['role'],
                        department=user_data['department'],
                        user_metadata={'auto_created': True}
                    )
                    user.set_password(user_data['password'])
                    db.session.add(user)
                    print(f"✅ Created user: {user_data['email']} ({user_data['role']})")
                
            db.session.commit()
            
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")

# Initialize database on import
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=False)
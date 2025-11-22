# Syllabus Tracker

A Flask-based web application for tracking and managing academic syllabi with role-based dashboards for students, teachers, HODs, and coordinators.

## Features

- **Role-Based Access Control**: Different dashboards for students, teachers, HODs, and coordinators
- **Authentication**: Secure login/registration with password hashing
- **Subject Management**: Track subjects, topics, and completion status
- **Progress Tracking**: Monitor student progress across enrolled subjects
- **Department Management**: Organize courses by department and academic year
- **Responsive Design**: Mobile-friendly interface with CSS design tokens

## Tech Stack

- **Backend**: Flask 3.0, SQLAlchemy 2.0, Flask-Login
- **Database**: MySQL with mysql-connector-python
- **Frontend**: Jinja2 templates, vanilla JavaScript, CSS3
- **Security**: Werkzeug password hashing, CSRF protection via Flask-WTF

## Project Structure

```
syllabus-tracker-fresh/
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # SQLAlchemy models
│   │   ├── user.py
│   │   ├── subject.py
│   │   ├── topic.py
│   │   └── ...
│   ├── blueprints/           # Flask blueprints
│   │   ├── auth/             # Authentication routes
│   │   ├── main/             # Main site routes
│   │   ├── api/              # REST API endpoints
│   │   └── dashboard/        # Role-based dashboards
│   ├── templates/            # Jinja2 templates
│   └── static/               # CSS, JS, images
├── scripts/                  # Utility scripts
│   ├── create_db.py         # Create tables & seed data
│   ├── reset_db.py          # Drop and recreate tables
│   ├── add_user.py          # Add test users
│   └── test_db_connection.py # Test DB connectivity
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+ (recommended; 3.13 has SQLAlchemy compatibility issues)
- MySQL 8.0+
- Virtual environment tool (venv)

### 1. Clone/Navigate to Project

```powershell
cd D:\syllabus-tracker-fresh
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment

Edit `.env` file with your MySQL credentials:

```env
SECRET_KEY=your-secret-key-here-change-me
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DB=syllabus_tracker
FLASK_APP=app
FLASK_ENV=development
ENABLE_CLAUDE_HAIKU_45=false
```

### 5. Create MySQL Database

In MySQL Workbench or CLI:

```sql
CREATE DATABASE syllabus_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Create Tables & Seed Data

```powershell
$env:PYTHONPATH = 'D:\syllabus-tracker-fresh'
$env:SEED = '1'
python .\scripts\create_db.py
```

This creates:
- Admin user: `admin@example.com` / `ChangeMe123!`
- Student user: `student1@example.com` / `Student123!`
- Sample department, course, subject, and topic

### 7. Verify Database

```powershell
python .\scripts\test_db_connection.py
```

Should show tables and user count > 0.

### 8. Run the Application

```powershell
flask run
```

Visit: `http://127.0.0.1:5000`

## Common Commands

### Add a User

```powershell
$env:PYTHONPATH = 'D:\syllabus-tracker-fresh'
python .\scripts\add_user.py --name "John Doe" --email "john@example.com" --password "Pass123!" --role student --department CSE
```

### Reset Database (DEV ONLY)

```powershell
$env:PYTHONPATH = 'D:\syllabus-tracker-fresh'
python .\scripts\reset_db.py --yes
```

### Test API Health

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5000/api/health
```

## User Roles

- **student**: View enrolled subjects and track progress
- **teacher**: Manage subjects and update topic completion
- **hod**: Department-wide oversight and faculty management
- **coordinator**: Multi-department analytics and reporting

## Key Fixes in This Version

- ✅ `password_hash` column increased to VARCHAR(255) to accommodate modern hash algorithms
- ✅ Added missing `phone`, `profile_image`, `is_active` columns to User model
- ✅ Fixed import to use `urllib.parse.urlparse` instead of deprecated werkzeug API
- ✅ Clean `.env` file with proper key=value format
- ✅ Complete model set with relationships (Department, Course, AcademicYear, etc.)
- ✅ Utility scripts for DB management and testing

## Development Notes

- Currently using `db.create_all()` for schema creation
- For production, set up Alembic migrations via Flask-Migrate
- Update `SECRET_KEY` in production to a strong random value
- Never commit `.env` file to version control

## Next Steps

- [ ] Set up Alembic migrations
- [ ] Implement full REST API endpoints
- [ ] Add file upload for syllabus documents
- [ ] Build interactive progress charts
- [ ] Add unit tests
- [ ] Set up CI/CD pipeline
- [ ] Implement rate limiting and security hardening

## 🚀 Deployment

### Cloud Deployment Options

#### 1. Heroku (Recommended for beginners)
```bash
# Install Heroku CLI, then:
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secure-secret-key
git push heroku main
```

#### 2. Railway/Render (Modern platforms)
1. Connect your GitHub repository
2. Set environment variables:
   - `SECRET_KEY`: Your secure secret key
   - `DATABASE_URL`: PostgreSQL connection string (auto-provided)
3. Deploy automatically on git push

#### 3. Docker Deployment
```bash
docker build -t syllabus-tracker .
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://... \
  syllabus-tracker
```

### Environment Variables

Required for production:
- `SECRET_KEY`: Secure secret key for sessions
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_COOKIE_SECURE`: Set to 'true' for HTTPS

### Production Checklist
- ✅ Gunicorn WSGI server configured
- ✅ PostgreSQL support added  
- ✅ Environment variables configured
- ✅ Security settings enabled
- ✅ Static file optimization ready

## License

MIT License (or your preferred license)

## Support

For issues or questions, please open an issue in the repository.

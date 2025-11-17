import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Database configuration - supports both local and cloud databases
    # Priority: DATABASE_URL (cloud) > individual MySQL config (local)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Cloud database (PostgreSQL, MySQL, etc.)
        # Fix for Heroku postgres:// → postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local MySQL configuration
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
        MYSQL_DB = os.environ.get('MYSQL_DB', 'syllabus_tracker')
        SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }
    
    # Feature flags
    ENABLE_CLAUDE_HAIKU_45 = os.environ.get('ENABLE_CLAUDE_HAIKU_45', 'false').lower() in ('1','true','yes','on')

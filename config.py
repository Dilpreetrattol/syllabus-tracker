import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'

    # Local MySQL configuration only
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'syllabus_tracker')

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Feature flags
    ENABLE_CLAUDE_HAIKU_45 = os.environ.get('ENABLE_CLAUDE_HAIKU_45', 'false').lower() in ('1','true','yes','on')

    # Email / SMTP settings (optional)
    EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED', 'false').lower() in ('1','true','yes','on')
    EMAIL_SERVER = os.environ.get('EMAIL_SERVER', '')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() in ('1','true','yes','on')
    EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'false').lower() in ('1','true','yes','on')
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER', os.environ.get('EMAIL_USERNAME', ''))

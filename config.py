import os
from dotenv import load_dotenv

# Load environment variables from .env file
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-citypulse-key-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(base_dir, 'app/static/uploads/images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

class DevelopmentConfig(Config):
    """Development configuration using local SQLite."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(base_dir, 'citypulse_dev.db')

class ProductionConfig(Config):
    """Production configuration using MySQL."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or \
        'mysql+pymysql://user:password@localhost/citypulse_prod'

# Dictionary to easily map environment names to config classes
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
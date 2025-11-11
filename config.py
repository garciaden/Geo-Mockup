from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

class Config:
    """Base configuration with common settings"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    WTF_CSRF_ENABLED = True

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "postgresql://culs_user:development_password@localhost:5432/culs_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries in console
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,          # Verify connections before using
        "pool_recycle": 300,            # Recycle connections after 5 minutes
        "pool_size": 10,                # Connection pool size
        "max_overflow": 20              # Max overflow connections
    }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Show SQL queries in development

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disabled for testing
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
        "postgresql://culs_user:development_password@localhost:5432/culs_test_db"

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    # Production should use strong secret key from environment
    # Validation happens at app initialization, not import time
    @property
    def validate_secret_key(self):
        if not os.environ.get("SECRET_KEY"):
            raise ValueError("SECRET_KEY environment variable must be set in production")
        return True

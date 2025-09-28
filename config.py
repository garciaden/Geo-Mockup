from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    WTF_CSRF_ENABLED = True
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False  # usually disabled for testing

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
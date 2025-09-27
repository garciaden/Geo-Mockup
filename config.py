from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "fallback-key"
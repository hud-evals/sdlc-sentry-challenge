import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Application settings
APP_NAME = os.getenv("APP_NAME", "Team Task Tracker")
APP_VERSION = "0.1.0"
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

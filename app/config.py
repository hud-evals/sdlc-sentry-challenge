import os

# Database configuration
# Read from environment variable, fallback to SQLite for local development
POSTGRES_URI = os.getenv("POSTGRES_URI", "sqlite:///./dev.db")

# Application settings
APP_NAME = os.getenv("APP_NAME", "Team Task Tracker")
APP_VERSION = "0.1.0"
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Sentry configuration
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "development")
SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

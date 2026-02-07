from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A team task tracking API for managing organizations, users, and tasks.",
)


@app.get("/")
def root():
    return {"name": APP_NAME, "version": APP_VERSION, "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

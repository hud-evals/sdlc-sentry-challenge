from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION
from app.routers import organizations, tasks, users

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="A team task tracking API for managing organizations, users, and tasks.",
)

# Include routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"name": APP_NAME, "version": APP_VERSION, "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

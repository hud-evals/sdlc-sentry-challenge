# Team Task Tracker API

A RESTful API for managing teams, organizations, and tasks. Built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Organization management (CRUD)
- User management with organization membership
- Task tracking with status, priority, and assignment
- Automatic error tracking via Sentry
- Database migrations with Alembic

## Quick Start

### Using Docker Compose (recommended)

```bash
# Start all services
docker compose up -d --build

# The API will be available at http://localhost:8001
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## API Endpoints

### Organizations
- `GET /api/v1/organizations/` — List organizations
- `POST /api/v1/organizations/` — Create organization
- `GET /api/v1/organizations/{id}` — Get organization
- `DELETE /api/v1/organizations/{id}` — Delete organization

### Users
- `GET /api/v1/users/` — List users
- `POST /api/v1/users/` — Create user
- `GET /api/v1/users/{id}` — Get user
- `DELETE /api/v1/users/{id}` — Delete user

### Tasks
- `GET /api/v1/tasks/` — List tasks (filter by status, priority, org, assignee)
- `POST /api/v1/tasks/` — Create task
- `GET /api/v1/tasks/{id}` — Get task
- `PATCH /api/v1/tasks/{id}` — Update task
- `DELETE /api/v1/tasks/{id}` — Delete task

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `POSTGRES_URI` | PostgreSQL connection URL | `sqlite:///./dev.db` |
| `SENTRY_DSN` | Sentry DSN for error tracking | _(empty)_ |
| `SENTRY_ENVIRONMENT` | Sentry environment name | `development` |
| `APP_NAME` | Application name | `Team Task Tracker` |
| `DEBUG` | Enable debug mode | `true` |

## Database Migrations

```bash
# Run all pending migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Rollback last migration
alembic downgrade -1
```

## Tech Stack

- **FastAPI** — Modern async web framework
- **SQLAlchemy** — ORM and database toolkit
- **Alembic** — Database migrations
- **PostgreSQL** — Primary database
- **Sentry** — Error monitoring and performance tracking
- **Docker** — Containerization

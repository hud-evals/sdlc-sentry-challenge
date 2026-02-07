"""
Tests for the SDLC configuration bug fix.

These tests verify BEHAVIOR, not implementation details. Any fix that
makes alembic correctly target PostgreSQL (instead of falling back to
SQLite) when deployed via docker-compose will pass — regardless of
which env var names are used or how the fix is structured.
"""
import os
import re
import shutil
import subprocess
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_docker_compose_api_env():
    """
    Extract environment variables set for the 'api' service in
    docker-compose.yml.  Returns a dict {VAR: value}.
    Works with both dict-style and list-style YAML environment blocks.
    """
    import yaml

    with open("docker-compose.yml") as f:
        compose = yaml.safe_load(f)

    api_service = compose.get("services", {}).get("api", {})
    raw_env = api_service.get("environment", {})

    if isinstance(raw_env, list):
        env = {}
        for item in raw_env:
            if "=" in str(item):
                k, v = str(item).split("=", 1)
                env[k] = v
        return env

    if isinstance(raw_env, dict):
        return {k: str(v) for k, v in raw_env.items() if v is not None}

    return {}


def _find_postgres_url(env_dict):
    """Return (var_name, url) for the first env var containing a postgresql:// URL."""
    for key, value in env_dict.items():
        if "postgresql://" in str(value):
            return key, str(value)
    return None, None


def _find_alembic_bin():
    """Locate the alembic binary."""
    alembic_bin = shutil.which("alembic")
    if alembic_bin:
        return alembic_bin
    # Try the bin/ directory next to the running Python
    candidate = os.path.join(os.path.dirname(sys.executable), "alembic")
    if os.path.isfile(candidate):
        return candidate
    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_alembic_targets_postgres_with_docker_compose_env():
    """
    Integration test: when deployed via docker-compose, alembic must
    generate PostgreSQL DDL — not SQLite DDL.

    How it works:
    1. Reads docker-compose.yml to find the DB connection env var & value
    2. Runs `alembic upgrade head --sql` with that env var set
    3. Asserts the output contains PostgreSQL-specific DDL (SERIAL)

    This test is agnostic to env var naming — it discovers the correct
    name from docker-compose.yml. Any fix that makes alembic read the
    same env var that docker-compose provides will pass.
    """
    api_env = _get_docker_compose_api_env()
    db_var, db_url = _find_postgres_url(api_env)

    assert db_var and db_url, (
        "docker-compose.yml 'api' service must set an environment variable "
        "with a postgresql:// connection URL. "
        f"Found env vars: {api_env}"
    )

    alembic_bin = _find_alembic_bin()
    assert alembic_bin, (
        "alembic binary not found. Install with: pip install alembic"
    )

    # Run alembic in offline mode with the docker-compose env vars
    run_env = {**os.environ}
    run_env.update(api_env)

    result = subprocess.run(
        [alembic_bin, "upgrade", "head", "--sql"],
        capture_output=True,
        text=True,
        env=run_env,
    )

    output = result.stdout

    assert "CREATE TABLE" in output, (
        f"Alembic --sql produced no DDL. This usually means alembic "
        f"could not resolve a database URL at all.\n"
        f"stderr: {result.stderr[:500]}"
    )

    # SERIAL is PostgreSQL-specific auto-increment type.
    # SQLite uses INTEGER instead.
    assert "SERIAL" in output, (
        "Alembic generated SQLite DDL instead of PostgreSQL when given "
        f"the docker-compose env var '{db_var}'. This means alembic/env.py "
        "is not reading that env var and is falling back to the SQLite "
        "URL in alembic.ini.\n"
        f"DDL preview:\n{output[:400]}"
    )


def test_app_config_resolves_to_postgres():
    """
    When deployed with docker-compose env vars, the app's database
    config must resolve to a postgresql:// URL, not sqlite://.

    This executes app/config.py in a subprocess with docker-compose
    env vars set and checks what database URL it resolves to.
    """
    api_env = _get_docker_compose_api_env()
    db_var, db_url = _find_postgres_url(api_env)

    assert db_var, (
        "docker-compose.yml must provide a PostgreSQL connection URL"
    )

    # Build env with all docker-compose vars (filter out shell templates)
    run_env = {**os.environ}
    for k, v in api_env.items():
        if not str(v).startswith("${"):
            run_env[k] = str(v)

    # Execute config.py standalone and print any DB-like variables
    script = (
        "import os\n"
        "with open('app/config.py') as f:\n"
        "    source = f.read()\n"
        "ns = {'os': os, '__builtins__': __builtins__}\n"
        "exec(compile(source, 'app/config.py', 'exec'), ns)\n"
        "for name, val in ns.items():\n"
        "    if isinstance(val, str) and ('postgresql://' in val or 'sqlite://' in val):\n"
        "        print(f'{name}={val}')\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        env=run_env,
    )

    assert "postgresql://" in result.stdout, (
        "With docker-compose env vars set, app/config.py still resolves "
        "to SQLite instead of PostgreSQL. The app and alembic must both "
        "read the same env var so they target the same database.\n"
        f"Config output: {result.stdout.strip()}\n"
        f"Stderr: {result.stderr[:300]}"
    )


def test_priority_field_intact():
    """
    Guard test: the priority field must exist in the Task model and
    have a corresponding migration. This prevents an agent from
    'fixing' the error by simply removing the priority feature.
    """
    with open("app/models.py") as f:
        models_content = f.read()

    assert "priority" in models_content, (
        "Task model must have a 'priority' field — removing it is not a valid fix"
    )

    migration_dir = "alembic/versions"
    assert os.path.isdir(migration_dir), "alembic/versions directory must exist"

    migration_files = os.listdir(migration_dir)
    has_priority_migration = any(
        "priority" in f.lower() for f in migration_files
    )
    assert has_priority_migration, (
        "A migration for the priority column must exist in alembic/versions/"
    )

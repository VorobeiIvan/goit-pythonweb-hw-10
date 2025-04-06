import subprocess
import pytest


def test_entrypoint_script():
    """
    Test if the entrypoint script runs without errors.
    """
    try:
        result = subprocess.run(
            ["bash", "./docker-entrypoint.sh"],
            capture_output=True,
            text=True,
            env={
                "POSTGRES_SERVER": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "password",
            },
        )
        assert result.returncode == 0
        assert "PostgreSQL is up and running!" in result.stdout
    except Exception as e:
        pytest.fail(f"Entrypoint script failed: {e}")

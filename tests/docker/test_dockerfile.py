import subprocess
import pytest


@pytest.fixture(scope="module")
def docker_compose_up():
    """
    Bring up the docker-compose services.
    """
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    yield
    subprocess.run(["docker-compose", "down"], check=True)


def test_services_running(docker_compose_up):
    """
    Test if all services in docker-compose are running.
    """
    result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
    assert "fastapi_app" in result.stdout
    assert "postgres_db" in result.stdout
    assert "redis_cache" in result.stdout

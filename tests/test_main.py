from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


def test_health_check():
    """
    Test the /health endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("main.initialize_database")
def test_startup_event(mock_initialize_database):
    """
    Test that the startup event initializes the database.
    """
    with TestClient(app) as client:
        # Startup event is triggered when TestClient is initialized
        mock_initialize_database.assert_called_once()


def test_middlewares():
    """
    Test that all middlewares are added to the application.
    """
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    from fastapi.middleware.cors import CORSMiddleware
    from slowapi.middleware import SlowAPIMiddleware

    assert CORSMiddleware in middleware_classes
    assert SlowAPIMiddleware in middleware_classes


def test_routers():
    """
    Test that all routers are added to the application.
    """
    routes = [route.path for route in app.routes]

    # Example routes from the routers
    assert "/auth/token" in routes  # From auth router
    assert "/contacts/" in routes  # From contacts router
    assert "/users/" in routes  # From users router

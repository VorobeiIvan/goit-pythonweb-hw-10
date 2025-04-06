from fastapi import FastAPI
from app.core.routers import add_routers


def test_add_routers():
    """
    Test that all routers are added to the FastAPI application.
    """
    app = FastAPI()
    add_routers(app)

    routes = [route.path for route in app.routes]

    assert "/auth/token" in routes  # Example route from auth
    assert "/contacts/" in routes  # Example route from contacts
    assert "/users/" in routes  # Example route from users

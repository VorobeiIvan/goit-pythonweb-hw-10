from fastapi import FastAPI
from app.core.middleware import add_middlewares
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware


def test_add_middlewares():
    """
    Test that all middleware are added to the FastAPI application.
    """
    app = FastAPI()
    add_middlewares(app)

    middleware_classes = [middleware.cls for middleware in app.user_middleware]

    assert CORSMiddleware in middleware_classes
    assert SlowAPIMiddleware in middleware_classes

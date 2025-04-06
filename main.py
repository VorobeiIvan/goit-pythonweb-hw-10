from fastapi import FastAPI
from app.core.middleware import add_middlewares
from app.core.exception_handlers import add_exception_handlers
from app.core.routers import add_routers
from app.core.startup import initialize_database
import logging

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація FastAPI
app = FastAPI()


# Подія для створення таблиць у базі даних під час запуску
@app.on_event("startup")
async def startup():
    logger.info("Starting application...")
    initialize_database()
    logger.info("Application started successfully.")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.

    Returns:
        dict: A dictionary with the status of the application.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


# Виклик функцій
add_middlewares(app)
add_exception_handlers(app)
add_routers(app)

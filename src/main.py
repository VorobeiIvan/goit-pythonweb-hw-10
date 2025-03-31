from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.routers.auth import router as auth_router
from src.routers.contacts import router as contacts_router
from src.routers.users import router as users_router
from src.middleware.middleware import ConfigValidationMiddleware

# Завантаження змінних середовища
load_dotenv()

# Ініціалізація додатку
app = FastAPI()

# Реєстрація Middleware
app.add_middleware(ConfigValidationMiddleware)

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Реєстрація роутерів
app.include_router(auth_router)
app.include_router(contacts_router)
app.include_router(users_router)

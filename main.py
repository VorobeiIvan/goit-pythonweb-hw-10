from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.database.database import Base, engine
from app.routers import auth, contacts, users

# Ініціалізація FastAPI
app = FastAPI()

# Ініціалізація Limiter
limiter = Limiter(key_func=lambda request: request.client.host)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# Обробка перевищення ліміту
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )


# Подія для створення таблиць у базі даних під час запуску
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


# Додавання CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(users.router, prefix="/users", tags=["Users"])

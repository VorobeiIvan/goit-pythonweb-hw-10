from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.auth import get_password_hash
from app.utils.dependencies import get_current_user, get_db
from app.utils.limiter import limiter
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register/", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        request (Request): The HTTP request object.
        user (UserCreate): The user data for registration.
        db (Session): The database session.

    Returns:
        UserResponse: The created user data.

    Raises:
        HTTPException: If the user already exists.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        logger.warning(
            f"Registration failed: User with email {user.email} already exists."
        )
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User registered successfully: {user.email}")
    return new_user


@router.get("/me/", response_model=UserResponse, status_code=200)
@limiter.limit("10/minute")
def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the current authenticated user's information.

    Args:
        request (Request): The HTTP request object.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        UserResponse: The current user's data.
    """
    logger.info(f"Retrieved current user info: {current_user.email}")
    return current_user

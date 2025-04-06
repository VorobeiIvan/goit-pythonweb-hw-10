from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.auth import get_password_hash
from app.utils.dependencies import get_db
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.utils.dependencies import get_current_user
from app.services.cloudinary_service import upload_avatar

# Initialize the router for user-related endpoints
router = APIRouter()

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)


@router.post("/register/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data for registration.
        db (Session): The database session.

    Returns:
        UserResponse: The registered user data.

    Raises:
        HTTPException: If a user with the given email already exists.
    """
    # Check if the user already exists in the database
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create a new user instance
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False,
        role=user.role,
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the newly created user
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session.

    Returns:
        UserResponse: The user data.

    Raises:
        HTTPException: If the user is not found.
    """
    # Query the database for the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user data
    return user


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(limiter.limit("5/minute"))],
)
async def get_current_user_route(current_user=Depends(get_current_user)):
    """
    Retrieve the currently authenticated user with rate limiting.

    Args:
        current_user: The currently authenticated user.

    Returns:
        UserResponse: The data of the current user.
    """
    # Return the current user's data
    return current_user


@router.post("/avatar/", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update the avatar of the currently authenticated user.

    Args:
        file (UploadFile): The avatar file to upload.
        db (Session): The database session.
        current_user: The currently authenticated user.

    Returns:
        UserResponse: The updated user data.
    """
    # Upload the avatar to Cloudinary
    avatar_url = upload_avatar(file)

    # Update the user's avatar in the database
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)

    # Return the updated user data
    return current_user

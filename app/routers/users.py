from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.auth import get_password_hash
from app.services.cloudinary_service import upload_avatar
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


@router.post("/register/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
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
    return new_user


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/avatar/", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    avatar_url = upload_avatar(file)
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/", response_model=UserResponse, status_code=200)
def get_current_user_info(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return current_user


@router.put("/me/", response_model=UserResponse, status_code=200)
def update_current_user_info(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    current_user.email = user_data.email
    current_user.role = user_data.role
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me/", status_code=204)
def delete_current_user(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return None


@router.get("/", response_model=list[UserResponse], status_code=200)
def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(User).all()


@router.post("/verify/{token}", status_code=200)
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/reset-password/{token}", status_code=200)
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password reset successfully"}


@router.post("/send-verification-email/", status_code=200)
def send_verification_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Verification email sent successfully"}


@router.post("/send-password-reset-email/", status_code=200)
def send_password_reset_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password reset email sent successfully"}

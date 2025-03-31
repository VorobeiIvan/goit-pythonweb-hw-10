import cloudinary.uploader
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.models import User


def update_avatar(file, current_user: User, db: Session):
    try:
        upload_result = cloudinary.uploader.upload(file.file)
        current_user.avatar_url = upload_result["secure_url"]
        db.commit()
        db.refresh(current_user)
        return {
            "message": "Аватар успішно оновлено",
            "avatar_url": current_user.avatar_url,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Помилка завантаження аватару: {str(e)}"
        )

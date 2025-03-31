from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.utils.db.sessions import get_db
from src.utils.auth.auth_utils import get_current_user
from src.models.models import User
import cloudinary.uploader

# Ініціалізація роутера для користувача
router = APIRouter(prefix="/users", tags=["Користувачі"])


@router.put("/avatar/")
def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює аватар користувача, завантажуючи файл на Cloudinary.
    """
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

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from src.services.users import update_avatar
from src.utils.auth.auth_utils import get_current_user
from src.utils.db.sessions import get_db

router = APIRouter(prefix="/users", tags=["Користувачі"])


@router.put("/avatar/")
def update(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_avatar(file, current_user, db)

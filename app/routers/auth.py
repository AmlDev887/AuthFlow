import jwt
from fastapi import Depends,APIRouter
from sqlalchemy import select
import secrets
from app.database.db import DBconnection
from app.schemas.auth import AuthLogin
from app.models.users_model import Users
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.config import settings
from app.workers.celery_app import send_message

router = APIRouter(prefix="/auth",
                   tags=["auth"])

oauth2 = OAuth2PasswordBearer(token = "/token")
redis = settings.REDIS_URL

def code_generate(length: int = 10):
    """Генерация кода подтверждения"""

    upper = 10**length
    code = secrets.randbelow(upper)
    return f"{code:0{length}d}"

@router.post("/register")
async def login(user: AuthLogin, db:DBconnection):
    """Пройди авторизацию"""
    
    stmt = select(Users).where(Users.email == user.login)
    result = await db.execute(stmt)
    answer = result.scalars().one_or_none()
    try:
        if answer is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail = "Пользователь с этим email существует"
            )
        code = code_generate(6)
        send_message.delay(email = user.login,
                        username = user.username,
                        code = code,
                        body = "Код для подтверждения email",
                        template_name = "app.templates.authorization_code.html")
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="при отправке кода что-то пошло не так"
        )

    redis.set(name = f"verify_code:{user.login}",
              value = code,
              ex = 300)
    
    return {"message":"Код подтверждения отправлен в ваш email"}

@router.post("/verify-otp")
async def verify_user()

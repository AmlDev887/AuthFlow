import jwt
import secrets
from sqlalchemy import select
from app.core.config import settings
from fastapi import Depends,APIRouter
from argon2 import PasswordHasher
from app.models.users_model import Users
from app.database.db import DBconnection
from fastapi import HTTPException, status
from argon2.exceptions import VerifyMismatchError
from app.workers.celery_app import send_message
from app.schemas.auth import AuthLogin, AuthVerify
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(prefix="/auth",
                   tags=["auth"])

oauth2 = OAuth2PasswordBearer(token = "/token")
redis = settings.REDIS_URL

ph = PasswordHasher()

def code_generate(length: int = 10):
    """Генерация кода подтверждения"""

    upper = 10**length
    code = secrets.randbelow(upper)
    return f"{code:0{length}d}"

def hash_password(password):
    """Хешируем полученный пароль"""
    hashed_password = ph.hash(password)
    return hashed_password

def verify_password(password,hash):
    """Проверяем пароль"""
    try:
        ph.verify(password,hash)
        return True
    except VerifyMismatchError:
        return False
#------------- создание токена-----------------

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
    kimmi = Users(
        email = user.email,
        username = user.username,
        hash_password = hash_password(user.password),
        is_active = True
    )

    db.add(kimmi)
    await db.commit()
    await db.refresh(kimmi)
    
    return {"message":"Код подтверждения отправлен в ваш email"}

@router.post("/verify-otp", status_code = status.HTTP_201_CREATED)
async def verify_user(send_code: AuthVerify,
                      db:DBconnection):
    """Проверка кода"""

    stmt = select(Users).where(Users.email == send_code.email, Users.is_active == True)
    result = await db.execute(stmt)
    answer = result.scalars().one_or_none()

    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Пользователь не найден"
        )
    cool_code = redis.get(name = f"verify_code:{send_code.email}")
    if cool_code is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Время кода истек либо неверный"
        )
    
    db.add(Users(is_verify = True))
    await db.commit






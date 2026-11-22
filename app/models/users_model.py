from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer,String,DateTime,func, Boolean
from datetime import datetime, timezone
from app.schemas.enums import UsersRole
from enum import Enum

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(225), unique=True, nullable=True)
    username:Mapped[str] = mapped_column(String(225), nullable = True)
    hash_password:Mapped[str] = mapped_column(String(225), nullabble=True) 
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable = False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified:Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    role:Mapped[UsersRole] = mapped_column(Enum())

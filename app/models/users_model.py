from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime, timezone

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(225), unique=True, nullable=True)
    username:Mapped[str] = mapped_column(String(225), nullable = True)
    hash_password:Mapped[str] = mapped_column(String(225), nullabble=True) 
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable = False)

    
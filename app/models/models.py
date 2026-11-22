from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime
from app.database.db import Base

class Task(Base):
    __tablename__ = "task"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String(225), unique=True)
    status:Mapped[bool] = mapped_column(default=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())



from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession,AsyncAttrs
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

DATABASE = settings.DATABASE
PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME
DB_PORT = settings.DB_PORT

DATABASE_URL = f"postgresql+asyncpg://{DATABASE}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session

DBconnection = Annotated[AsyncSession, Depends(get_db)]


class Base(AsyncAttrs,DeclarativeBase):
    pass
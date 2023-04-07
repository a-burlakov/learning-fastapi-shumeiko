from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import DeclarativeBase

from config import DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
from models.models import role

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base: DeclarativeBase = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    # email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    # hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    registered_at = Column(
        "registered_at", TIMESTAMP, default=datetime.utcnow, nullable=False
    )
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

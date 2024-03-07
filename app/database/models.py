from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import SQLALCHEMY_URL


engine = create_async_engine(SQLALCHEMY_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    VIEW = "v"
    CHATING = "c"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    tg_id = mapped_column(BigInteger, unique=True)
    status = mapped_column(String, default=VIEW)

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    tg_id = mapped_column(BigInteger, unique=True)
    user_id = mapped_column(ForeignKey("users.id"))

class Character_2(Base):
    __tablename__ = "characters_2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name = mapped_column(String)
    age = mapped_column(String)
    sex = mapped_column(String)
    description = mapped_column(String)
    short_description = mapped_column(String)

class Token(Base):
    __tablename__ = "tokens"

    WORK = "w"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    status = mapped_column(String)
    token = mapped_column(String)

class Form(Base):
    __tablename__ = "forms"

    M = "male"
    F = "female"
    B = "bi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    user = mapped_column(ForeignKey("users.id"))

    name = mapped_column(String)
    age = mapped_column(String)
    sex = mapped_column(String)
    description = mapped_column(String)

    target = mapped_column(String)

class Chat(Base):
    __tablename__ = "chats"

    ACTIVE = "ac"
    ARCHIVED = "ar"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    tg_id = mapped_column(BigInteger)

    status = mapped_column(String, default=ACTIVE)
    messages = mapped_column(String, default="[]")

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

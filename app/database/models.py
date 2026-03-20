from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, Column, Integer
from pgvector.sqlalchemy import Vector

from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "user_account"
    id: int = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    telegram_id: int = Field(unique=True)
    gender: str = Field(nullable=True)
    name: str = Field(nullable=True)
    age: int = Field(nullable=True)
    city: str = Field(nullable=True)
    gar_city: str = Field(nullable=True)
    bio: str = Field(nullable=True)
    bio_vector: Optional[List[float]] = Field(
        sa_column=Column(Vector(384))
    )
    status: str = Field(default="inactive")
    deleted: bool = Field(default=False)

    filter: Optional["UserFilter"] = Relationship(back_populates="user")
    media: List["UserMedia"] = Relationship(back_populates="user")


class UserFilter(SQLModel, table=True):
    __tablename__ = "user_filter"
    id: int = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    target_gender: str = Field(nullable=True)
    min_age: int = Field(default=16)
    max_age: int = Field(default=99)
    target_city: str = Field(nullable=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_account.id", ondelete="CASCADE"), unique=True)
    )

    user: Optional["User"] = Relationship(back_populates="filter")


class UserMedia(SQLModel, table=True):
    __tablename__ = "user_media"
    id: int = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    file_id: str
    unique_file_id: str
    file_type: str = Field(default="photo")
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_account.id", ondelete="CASCADE"))
    )

    user: Optional["User"] = Relationship(back_populates="media")

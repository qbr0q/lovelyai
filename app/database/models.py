from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, Column, Integer
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "user_account"
    id: int = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    telegram_id: int = Field(unique=True)
    gender: str
    name: str
    age: int
    city: str
    bio: str
    status: str
    deleted: bool = Field(default=False)

    filter: Optional["UserFilter"] = Relationship(back_populates="user")


class UserFilter(SQLModel, table=True):
    __tablename__ = "user_filter"
    id: int = Field(default=None, primary_key=True)
    create_date: datetime = Field(default_factory=datetime.now)
    target_gender: str = Field(nullable=True)
    min_age: int = Field(default=16)
    max_age: int = Field(default=99)
    target_city: str = Field(nullable=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_account.id", ondelete="CASCADE"))
    )

    user: Optional["User"] = Relationship(back_populates="filter")

from sqlmodel import SQLModel, Field
from datetime import datetime


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

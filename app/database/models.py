from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, Column, Integer, DateTime, func, UniqueConstraint, Index, BigInteger
from pgvector.sqlalchemy import Vector
from datetime import datetime
from typing import Optional, List
from .enums import UserStatus


class User(SQLModel, table=True):
    __tablename__ = "user_profile"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(),
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now()
        )
    )
    telegram_id: int = Field(sa_column=Column(BigInteger, unique=True))
    username: str = Field(nullable=True)
    gender: str = Field(nullable=True)
    name: str = Field(nullable=True)
    age: int = Field(nullable=True)
    city: str = Field(nullable=True)
    gar_city: str = Field(nullable=True, index=True)
    bio: str = Field(nullable=True)
    bio_vector: Optional[List[float]] = Field(
        sa_column=Column(Vector(384))
    )
    status: str = Field(default="inactive")
    deleted: bool = Field(default=False)

    filter: Optional["UserFilter"] = Relationship(back_populates="user")
    media: List["UserMedia"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        }
    )
    match_received: List["MatchAction"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MatchAction.to_user_id]", "back_populates": "to_user"}
    )
    ai_request: List["AIRequestLog"] = Relationship(back_populates="user")

    def clear(self):
        self.status = UserStatus.inactive
        self.gender = ""
        self.name = ""
        self.age = 0
        self.city = ""
        self.gar_city = ""
        self.bio = ""
        self.bio_vector = None

        self.media = []
        self.filter.clear()

    @property
    def is_empty(self):
        return self.name is None and self.gender is None and \
                    self.age is None and self.city is None and self.bio is None


class UserFilter(SQLModel, table=True):
    __tablename__ = "user_filter"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(),
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now()
        )
    )
    target_gender: str = Field(nullable=True)
    min_age: int = Field(nullable=True)
    max_age: int = Field(nullable=True)
    target_city: str = Field(nullable=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), unique=True)
    )

    user: Optional["User"] = Relationship(back_populates="filter")

    def clear(self):
        self.target_gender = ""
        self.min_age = 16
        self.max_age = 99
        self.target_city = ""


class UserMedia(SQLModel, table=True):
    __tablename__ = "user_media"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    file_id: str
    file_unique_id: str
    file_type: str = Field(default="photo")
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    )

    user: Optional["User"] = Relationship(back_populates="media")


class MatchAction(SQLModel, table=True):
    __tablename__ = "match_action"
    __table_args__ = (
        # ускоряет проверку "кто кого оценил" в разы, не дает лайкнуть одного и того же человека дважды
        UniqueConstraint("from_user_id", "to_user_id", name="unique_match_action"),
        Index("ix_match_action_to_user", "to_user_id"),
    )
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    from_user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    )
    to_user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    )
    action: str = Field(index=True)
    is_match: bool = Field(default=None, nullable=True)

    from_user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MatchAction.from_user_id]"}
    )
    to_user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MatchAction.to_user_id]"}
    )


class AIRequestLog(SQLModel, table=True):
    __tablename__ = "ai_request_log"

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    action_type: str
    prompt_text: str
    completion_text: str
    tokens_used: int = Field(index=True)
    response_time: int = Field(index=True)
    model_name: str
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    )

    user: Optional["User"] = Relationship(back_populates="ai_request")

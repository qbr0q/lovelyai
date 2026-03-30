from pydantic import BaseModel


class MatchProfileMedia(BaseModel):
    file_id: str

    class Config:
        from_attributes = True


class MatchProfile(BaseModel):
    id: int
    telegram_id: int
    name: str | None = None
    age: int | None = None
    city: str | None = None
    gar_city: str | None = None
    bio: str | None = None
    media: list[MatchProfileMedia] = []
    match_percent: str | None = None

from pydantic import BaseModel


class MatchProfileMedia(BaseModel):
    file_id: str

    class Config:
        from_attributes = True


class MatchProfile(BaseModel):
    id: int
    telegram_id: int
    name: str
    age: int
    city: str
    gar_city: str
    bio: str
    media: list[MatchProfileMedia] = []
    match_percent: str | None = None

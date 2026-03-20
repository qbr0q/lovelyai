from typing import Optional, List
from pydantic import BaseModel


class SimpleObject:
    def __init__(self, **kwargs):
        for i, v in kwargs.items():
            setattr(self, i, v)

    def __getattr__(self, item):
        return self.__dict__.get(item)


class Profile(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    gar_city: Optional[str] = None
    bio: Optional[str] = None
    bio_vector: Optional[List[float]] = None
    media: List[str] = []

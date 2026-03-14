from dataclasses import dataclass, asdict


class SimpleObject:
    def __init__(self, **kwargs):
        for i, v in kwargs.items():
            setattr(self, i, v)

    def __getattr__(self, item):
        return self.__dict__.get(item)


@dataclass
class Profile:
    name: str = ""
    age: int = 0
    gender: str = ""
    city: str = ""
    bio: str = ""

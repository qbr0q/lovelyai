from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"


# class ActionType(str, Enum):
#     like = "like"
#     dislike = "dislike"

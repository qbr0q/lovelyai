from enum import StrEnum


class UserStatus(StrEnum):
    active = "active"
    inactive = "inactive"
    banned = "banned"


class ActionType(StrEnum):
    like = "like"
    dislike = "dislike"


class QueueName(StrEnum):
    MATCH = "match:queue"
    CURRENT_MATCH = "current-match:queue"
    RECEIVED_LIKE = "like-received:queue"
    CURRENT_RECEIVED_LIKE = "current-like-received:queue"


class AiRequestType(StrEnum):
    create_profile = "create_profile"


class MediaType(StrEnum):
    photo = "photo"


class UserRole(StrEnum):
    user = "user"
    admin = "admin"

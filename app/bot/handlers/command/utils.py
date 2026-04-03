from app.database.models import User, UserFilter


def create_user(user):
    user = User(
        telegram_id=user.telegram_id,
        username=user.username
    )
    user.filter = UserFilter(
        telegram_id=user.telegram_id
    )
    return user

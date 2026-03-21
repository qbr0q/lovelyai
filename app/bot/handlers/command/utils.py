from app.database.models import User, UserFilter


def create_user(telegram_id):
    user = User(
        telegram_id=telegram_id
    )
    user.filter = UserFilter(
        telegram_id=telegram_id
    )
    return user

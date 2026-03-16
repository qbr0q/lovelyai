from app.database.models import User


def create_user(session, telegram_id):
    user_record = User(
        telegram_id=telegram_id
    )
    session.add(user_record)
